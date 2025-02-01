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

#### Windows Users:

1. Install Python if you haven’t already: Download Python

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
#### Mac/Linux Users:

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

