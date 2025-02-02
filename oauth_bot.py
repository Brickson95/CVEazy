import json
import requests
import discord
import asyncio
from aiohttp import ClientSession

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]
REDIRECT_URI = config["redirect_uri"]
USER_ID = config["user_id"]
NVD_FEED_URL = "https://www.cve.org/api/?action=getCveRecent"

TOKEN_URL = "https://discord.com/api/oauth2/token"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

SEVERITY_COLORS = {
    "LOW": 0x2ECC71,  # Green
    "MEDIUM": 0xF1C40F,  # Yellow
    "HIGH": 0xE67E22,  # Orange
    "CRITICAL": 0xE74C3C  # Red
}

async def load_tokens():
    """Load tokens from tokens.json"""
    try:
        with open("tokens.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

async def refresh_token():
    """Refresh the OAuth2 access token"""
    tokens = await load_tokens()
    if not tokens:
        print("No tokens found. User needs to authorize the bot.")
        return None

    async with ClientSession() as session:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"]
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with session.post(TOKEN_URL, data=data, headers=headers) as resp:
            new_tokens = await resp.json()

            if "access_token" in new_tokens:
                print("✅ Token refreshed successfully.")
                await save_tokens(new_tokens)
                return new_tokens["access_token"]
            else:
                print("❌ Failed to refresh token:", new_tokens)
                return None

async def get_access_token():
    """Ensure we have a valid access token (refresh if necessary)"""
    tokens = await load_tokens()
    if not tokens:
        return None

    return await refresh_token()

async def send_message(user, message, embed=None):
    """Send a DM to the user using OAuth2 token"""
    access_token = await get_access_token()
    if not access_token:
        print("❌ No valid access token. Unable to send message.")
        return

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {"recipient_id": str(USER_ID), "content": message}
    
    if embed:
        data["embeds"] = [embed.to_dict()]

    async with ClientSession() as session:
        async with session.post("https://discord.com/api/v10/users/@me/channels", json={"recipient_id": str(USER_ID)}, headers=headers) as resp:
            if resp.status == 200:
                channel = await resp.json()
                channel_id = channel["id"]

                async with session.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", json=data, headers=headers) as msg_resp:
                    if msg_resp.status == 200:
                        print("✅ Message sent successfully!")
                    else:
                        print(f"❌ Failed to send message: {msg_resp.status}, {await msg_resp.text()}")

async def fetch_cves():
    """Fetch recent CVEs and send them to the user"""
    response = requests.get(NVD_FEED_URL)
    if response.status_code == 200:
        cves = response.json().get('CVE_Items', [])
        for cve in cves[:3]:
            cve_id = cve.get('cve_id', 'Unknown ID')
            description = cve.get('description', 'No description available')
            published_date = cve.get('published_date', 'Unknown date')

            embed = discord.Embed(
                title=f"New CVE Alert: {cve_id}",
                description=description,
                color=SEVERITY_COLORS.get("UNKNOWN", 0x95A5A6)
            )
            embed.add_field(name="📅 Published", value=published_date, inline=False)
            embed.add_field(name="🔗 More Info", value=f"[CVE.org Link](https://www.cve.org/cverecord?id={cve_id})", inline=False)

            await send_message(USER_ID, "", embed)
    else:
        print(f"❌ Failed to fetch CVEs: {response.status_code}")

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    while True:
        await fetch_cves()
        await asyncio.sleep(3600)  # Fetch CVEs every hour

client.run(config["bot_token"])

