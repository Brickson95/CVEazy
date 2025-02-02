import discord
import requests
import asyncio
import json

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config.get("token")  # Fetch token from config.json
USER_ID = config.get("user_id")  # Fetch user ID from config.json
NVD_FEED_URL = "https://www.cve.org/api/?action=getCveRecent"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
'''
# Define colors for different severity levels
SEVERITY_COLORS = {
    "LOW": 0x2ECC71,        # Green
    "MEDIUM": 0xF1C40F,     # Yellow
    "HIGH": 0xE67E22,       # Orange
    "CRITICAL": 0xE74C3C    # Red
}

def get_severity(cve):
    """Extract severity level from CVE data."""
    impact = cve.get('impact', {})
    base_score = None
    severity = "UNKNOWN"

    if "baseMetricV3" in impact:
        base_score = impact["baseMetricV3"]["cvssV3"]["baseScore"]
    elif "baseMetricV2" in impact:
        base_score = impact["baseMetricV2"]["cvssV2"]["baseScore"]

    if base_score is not None:
        if base_score < 4.0:
            severity = "LOW"
        elif base_score < 7.0:
            severity = "MEDIUM"
        elif base_score < 9.0:
            severity = "HIGH"
        else:
            severity = "CRITICAL"

    return severity, base_score
'''
async def fetch_cves():
    await client.wait_until_ready()
    user = await client.fetch_user(USER_ID)

    response = requests.get(NVD_FEED_URL)
    if response.status_code == 200:
        cves = response.json().get('data', [])
        
        for cve in cves[:3]:  # Limit to 3 messages per fetch
            cve_id = cve.get('cve_id', 'Unknown ID')
            description = cve.get('description', 'No description available')
            published_date = cve.get('published_date', 'Unknown date')

            # severity, score = get_severity(cve)
            # color = SEVERITY_COLORS.get(severity, 0x95A5A6)  # Default gray if unknown

            embed = discord.Embed(
                title=f"New CVE Alert: {cve_id}",
                description=description,
                color=0xE67E22
            )
            embed.add_field(name="📅 Published", value=published_date, inline=False)
            # embed.add_field(name="⚠️ Severity", value=f"{severity} (Score: {score})", inline=False)
            embed.add_field(name="🔗 More Info", value=f"[CVE.org Link](https://www.cve.org/cverecord?id={cve_id})", inline=False)

            await user.send(embed=embed)
    else:
        print(f"Failed to fetch CVEs: {response.status_code}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    
    user = await client.fetch_user(USER_ID)  # Fetch user object
    if user:
        await user.send("✅ Bot is online and ready to send CVE updates!")
    
    while True:
        await fetch_cves()
        await asyncio.sleep(3600)  # Check every hour

client.run(TOKEN)
