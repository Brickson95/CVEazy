# Discord_CVE_Updater

Hey there! Want to get CVE alerts directly in your Discord inbox? Follow these super easy steps to set up your very own bot. No complicated tech talk – just simple instructions!

# 🚀 What This Bot Does

This bot will send you messages on Discord whenever a new CVE (Common Vulnerabilities and Exposures) is published. That way, you stay up to date with the latest security threats!

✅ Open-source and free

✅ Runs on your own computer (private & secure)

✅ Works 24/7 so you never miss an alert

# 🛠️ What You Need

* A computer (Windows, Mac, or Linux) OR a free cloud service (like Replit)

* Python installed (if running locally)

* A Discord account

# Setup

## 🔧 Step 1: Get the Bot Code

1. Go to GitHub: https://github.com/Brickson95/Discord_CVE_Updater

2. Click the green "Code" button.

3. Select "Download ZIP" and unzip the folder on your computer.

OR

If you have Git installed, you can run this command instead:
```
git clone https://github.com/Brickson95/Discord_CVE_Updater.git
```

## ⚙️ Step 2: Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)

2. Click "New Application" → Give it a name (e.g., "CVE Bot")

3. Go to "Bot" (left side menu) → Click "Add Bot"

4. Click "Reset Token" and copy the token (Keep it safe!)

5. Under "Privileged Gateway Intents," turn on "Message Content Intent"

6. Save your bot token for the next step!

## 📁 Step 3: Set Up the Bot

1. Inside the downloaded bot folder, create a new file called config.json

2. Open config.json and paste this:
```
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "user_id": "YOUR_DISCORD_USER_ID"
}
```
3. Replace YOUR_BOT_TOKEN_HERE with your actual bot token.

4. Replace YOUR_DISCORD_USER_ID with your Discord ID (find it by enabling Developer Mode and right-clicking your name → "Copy ID").

## 🏃 Step 4: Run the Bot (Locally)

### Windows Users:

1. Install Python if you haven’t already: [Download Python](https://www.python.org/downloads/)

2. Open Command Prompt (Win + R → type cmd → hit Enter)

3. Navigate to the bot folder:
```
cd path/to/Discord_CVE_Updater
```
4. Install required dependencies:
```
pip install -r requirements.txt
```
5. Start the bot:
```
python bot.py
```
### Mac/Linux Users:

1. Open Terminal.

2. Navigate to the bot folder:
```
cd path/to/Discord_CVE_Updater
```
4. Install required dependencies:
```
pip3 install -r requirements.txt
```
5. Start the bot:
```
python3 bot.py
```
## ☁️ Step 5: Run It 24/7 (Free Cloud Hosting)

If you don’t want to keep your computer on all the time, you can run this bot for free on Replit!

### Run on Replit (Easy & Free)

1. Go to [Replit](https://replit.com/) and create an account.

2. Click "Create Repl", choose Python, and create a new project.

3. Copy and paste the bot’s bot.py code into Replit.

4. Click "Files" (left menu), create a new file called config.json, and add:
```
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "user_id": "YOUR_DISCORD_USER_ID"
}
```
5. Click "Run" and your bot will start!

6. (Optional) Use [UptimeRobot](https://uptimerobot.com/) to keep it running 24/7.

## 🛠️ Troubleshooting

### "Bot is running, but I don’t get messages!"

* Check that you entered the correct user ID in config.json.

* Make sure your bot is online in the Discord Developer Portal.

* Ensure you enabled "Message Content Intent" in the bot settings.

### "Bot closes when I shut down my computer!"

* Use Replit or a cloud server if you want it online 24/7.

* If running locally, use screen (Linux/Mac) or Task Scheduler (Windows).
