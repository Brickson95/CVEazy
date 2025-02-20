import asyncio
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import aiohttp
import discord

CONFIG_FILE = "config.json"
LAST_CVE_ID_FILE = "last_cve_id.txt"
API_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RESULTS_PER_PAGE = '500'
CHECK_INTERVAL = 299 # seconds
RETRY_INTERVAL = 60  # seconds

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CVEazy:
    def __init__(self):
        self.config = self.load_config(CONFIG_FILE)
        self.TOKEN = self.config.get("bot_token")
        self.USER_ID = self.config.get("user_id")
        self.NVD_API_KEY = self.config.get("nvd_api")

        if not self.TOKEN or not self.USER_ID or not self.NVD_API_KEY:
            logging.critical(f"Missing required bot token, user ID, or NVD API Key. Exiting.")
            exit(1)

        self.intents = discord.Intents.default()
        self.client = MyClient(intents=self.intents, cveazy=self)

    def load_config(self, file_path):
        try:
            with open(self.sanitize_path(file_path), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.critical(f"Config file not found: {file_path}. Exiting.")
            exit(1)
        except json.JSONDecodeError as e:
            logging.critical(f"Error parsing '{file_path}': {e}. Exiting.")
            exit(1)

    def load_last_cve_id(self, file_path=LAST_CVE_ID_FILE):
        if os.path.exists(self.sanitize_path(file_path)):
            with open(file_path, "r") as f:
                return f.read().strip()
        return None
    
    def save_last_cve_id(self, cve_id, file_path=LAST_CVE_ID_FILE):
        with open(self.sanitize_path(file_path), "w") as f:
            f.write(cve_id)

    def sanitize_path(self, file_path):
        base_path = Path(__file__).parent.resolve()
        full_path = (base_path / file_path).resolve()
        if not full_path.is_relative_to(base_path):
            raise ValueError("Attempted path traversal detected.")
        return full_path

    async def fetch_cve_data(self, session, url, params, headers, retries=3, backoff_factor=1):
        for attempt in range(retries):
            try:
                async with session.get(url, params=params, headers=headers) as response:
                    logging.info(f"Status code: {response.status} - Constructed URL: {response.url}")
                    if response.status == 200:
                        data = await response.json()
                        return data
                    elif response.status == 403:
                        logging.error(f"HTTP error 403 Forbidden on attempt {attempt + 1} of {retries}")
                        if attempt < retries - 1:
                            sleep_time = backoff_factor * (2 ** attempt)
                            logging.info(f"Retrying in {sleep_time} seconds...")
                            await asyncio.sleep(sleep_time)
                            continue
                        else:
                            logging.error(f"Max retries reached. Giving up due to 403 errors.")
                            return None
                    else:
                        logging.error(f"HTTP error {response.status} while fetching CVEs.")
                        return None
            except asyncio.TimeoutError:
                logging.error(f"Timeout error on attempt {attempt + 1} of {retries}")
                if attempt < retries - 1:
                    sleep_time = backoff_factor * (2 ** attempt)
                    logging.info(f"Retrying in {sleep_time} seconds...")
                    await asyncio.sleep(sleep_time)
                    continue
                else:
                    logging.error(f"Max retries reached. Giving up due to timeout errors.")
                    return None
            except aiohttp.ClientError as e:
                logging.error(f"Client error: {e}")
                return None
            
    async def process_and_send_cve(self, user, cve_item, alert_type):
        try:
            cve_data = cve_item.get('cve', {})
            cve_id = cve_data.get('id', 'Unknown ID')
            descriptions = cve_data.get('descriptions', [])
            description = next((desc['value'] for desc in descriptions if desc['lang'] == 'en'), 'No description available')
            published_date = cve_data.get('published', 'N/A')
            references = cve_data.get('references', [])
            references_urls = [ref['url'] for ref in references] if references else []
            references_text = '\n'.join(references_urls) if references_urls else 'No references available'

            message = f"""
🚨 **{alert_type}**

**ID:** {cve_id}
**Description:** {description}
**Published Date:** {published_date}
**References:**
{references_text}

Stay vigilant! 🔒
"""
            await user.send(message)
            return cve_id
        except discord.Forbidden:
            logging.error(f"Could not send message to user {user.id}: Forbidden.")
            return None
        except discord.HTTPException as e:
            logging.error(f"HTTPException occurred: {e}")
            return None
        
    async def send_cve_updates(self):
        last_cve_id = self.load_last_cve_id()

        await self.client.wait_until_ready()
        try:
            user = await self.client.fetch_user(self.USER_ID)

            #Test sending a simple message
            await user.send("Hello! This is a test message from CVEazy.")
            logging.info(f"Test message sent successfully.")
        except discord.Forbidden as e:
            logging.error(f"Could not send test message to user {user.id}: Forbidden. {e}")

        timeout = aiohttp.ClientTimeout(total=45)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while not self.client.is_closed():
                try:
                    # Set end_time to current UTC time
                    end_time = datetime.now(timezone.utc)
                    # Set start_time to 5 minutes before end_time
                    start_time = end_time - timedelta(minutes=5)

                    # Format date strings
                    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

                    params = {
                        'pubStartDate': start_time_str,
                        'pubEndDate': end_time_str,
                        'resultsPerPage': RESULTS_PER_PAGE,
                        # Uncomment line below to only retrieve critical CVEs
                        # 'cvssV3Severity': 'CRITICAL'
                    }

                    headers = {
                        'User-Agent': 'CVEazy/1.0 (Contact: your_email@example.com)',
                        'apikey': self.NVD_API_KEY
                    }

                    data = await self.fetch_cve_data(session, API_BASE_URL, params, headers)
                    if data:
                        cve_items = data.get('vulnerabilities', [])
                        if not cve_items:
                            logging.info('No new CVEs in the last time window.')

                            # Fetch the most recent CVE
                            latest_end_time = datetime.now(timezone.utc)
                            latest_start_time = latest_end_time - timedelta(days=1)

                            latest_start_time_str = latest_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                            latest_end_time_str = latest_end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

                            params_latest = {
                                'pubStartDate': latest_start_time_str,
                                'pubEndDate': latest_end_time_str,
                                'resultsPerPage': RESULTS_PER_PAGE,
                                # Uncomment line below to only retrieve critical CVEs
                                # 'cvssV3Severity': 'CRITICAL'
                            }

                            data_latest = await self.fetch_cve_data(session, API_BASE_URL, params_latest, headers)
                            if data_latest:
                                cve_items_latest = data_latest.get('vulnerabilities', [])

                                if cve_items_latest:
                                    cve_items_latest.sort(key=lambda x: x['cve'].get('published', ''), reverse=True)

                                    cve_item = cve_items_latest[0]
                                    cve_data = cve_item.get('cve', {})
                                    cve_id = cve_data.get('id', 'Unknown ID')
                                    if cve_id != last_cve_id:
                                        last_cve_id = await self.process_and_send_cve(user, cve_item, "Most Recent CVE Alert")
                                        self.save_last_cve_id(last_cve_id)
                                    else:
                                        logging.info(f"No new CVEs available.")
                                else:
                                    logging.info('No CVEs found in the database.')
                            else:
                                logging.error(f"Failed to retrieve the most recent CVE data.")
                                await asyncio.sleep(RETRY_INTERVAL)
                                continue
                        else:
                            new_cves = []
                            for cve_item in cve_items:
                                cve_data = cve_item.get('cve', {})
                                cve_id = cve_data.get('id', 'Unknown ID')
                                if cve_id == last_cve_id:
                                    break
                                new_cves.append(cve_item)
                            
                            if new_cves:
                                for cve_item in new_cves:
                                    last_cve_id = await self.process_and_send_cve(user, cve_item, "New CVE Alert")
                                self.save_last_cve_id(last_cve_id)
                            else:
                                logging.info('No New CVEs at this time.')

                        await asyncio.sleep(CHECK_INTERVAL)

                    else:
                        logging.error(f"Failed to retrieve CVE data. Retrying after delay.")
                        await asyncio.sleep(RETRY_INTERVAL)
                        continue

                except aiohttp.ClientError as e:
                    logging.error(f"Request error occurred: {e}", exc_info=True)
                    await asyncio.sleep(RETRY_INTERVAL)
                except discord.errors.DiscordException as e:
                    logging.error(f"Discord error occurred: {e}", exc_info=True)
                    await asyncio.sleep(RETRY_INTERVAL)
                except Exception as e:
                    logging.error(f"An error occurred: {e}", exc_info=True)
                    await asyncio.sleep(RETRY_INTERVAL)

class MyClient(discord.Client):
    def __init__(self, intents, cveazy):
        super().__init__(intents=intents)
        self.cveazy = cveazy

    async def setup_hook(self):
        self.bg_task = self.loop.create_task(self.cveazy.send_cve_updates())

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_disconnect(self):
        logging.info('Bot disconnected.')

    async def on_error(self, event, *args, **kwargs):
        logging.error(f'An error occurred: {event}', exc_info=True)

    async def on_resumed(self):
        logging.info('Bot resumed.')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content == '!ping':
            await message.channel.send('Pong!')
