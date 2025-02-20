# Discord_CVE_Updater

Hey there! Want to get CVE alerts directly in your Discord inbox? Follow these super easy steps to set up your very own bot.

# 🚀 What This Bot Does

This bot will send you messages on Discord whenever a new CVE (Common Vulnerabilities and Exposures) is published. That way, you stay up to date with the latest security threats!

✅ Open-source and free

✅ Runs on your own computer (private & secure)

✅ Works 24/7 so you never miss an alert

# 🛠️ What You Need

* A computer (Windows, Mac, or Linux)

* Python installed (if running locally)

* A Discord account

# Setup

## 🔧 Step 1: Get the Bot Code

1. Go to GitHub: https://github.com/Brickson95/CVEazy

2. Click the green "Code" button.

3. Select "Download ZIP" and unzip the folder on your computer.

OR

If you have Git installed, you can run this command instead:
```
git clone https://github.com/Brickson95/CVEazy.git
```

## ⚙️ Step 2: Create a Discord Bot

1. Create a new server on Discord you'd like to add the bot too. The bot won't post anything on the server, so you can also add it to any server, as long as you have manage server permissions

2. Go to the [Discord Developer Portal](https://discord.com/developers/applications)

3. Click "New Application" → Give it a name (e.g., "CVE Bot")

4. Go to the "Bot" tab (left side menu)

5. Click "Reset Token" and copy the token (Keep it safe!)

6. Navigate to the "OAuth2" tab (left side menu)

7. In the "SCOPES" section of the "OAuth2 URL Generator" select the "bot" checkbox

8. Then, in the "Bot Permissions" section select the "Send Messages", "Embed Links", and "Attach Files" checkboxes

9. After selecting the appropriate boxes, copy the URL from the bottom of the "OAuth2 URL Generator", open a new tab, and paste the URL into the address bar

10. When the URL loads you will be greeted with a page to authorize your bot to use the permissions you granted it on the previous page
  
11. Select the server you'd like to add the bot too, and then click "Continue"

12. You should now see your bot as a member of your server

13. Save your bot token for the next step!

## 📁 Step 3: Set Up the Bot

1. Navigate to the [NVD developer portal](https://nvd.nist.gov/developers/request-an-api-key) and request an API key for personal use

2. Once you recieve the API key, keep it safe

3. Inside the downloaded bot folder, find the config.json file.

4. Open config.json and you'll see this:
```
{
  "bot_token": "YOUR_DISCORD_BOT_TOKEN",
  "user_id": "YOUR_DISCORD_USER_ID",
  "nvd_api": "YOUR_NVD_API_KEY"
}
```
5. Replace YOUR_BOT_TOKEN_HERE with your actual bot token from the previous step.

6. Replace YOUR_DISCORD_USER_ID with your Discord ID (find it by enabling Developer Mode and clicking your name → "Copy ID").

7. Replace YOUR_NVD_API_KEY with the API key you got earlier in this step.

## 🏃 Step 4: Run the Bot (Locally)

### Windows Users:

1. Install Python if you haven’t already: [Download Python](https://www.python.org/downloads/)

2. Open Command Prompt (Win + R → type cmd → hit Enter)

3. Navigate to the bot folder:
```
cd path/to/CVEazy
```
4. Install required dependencies:
```
pip install -r requirements.txt
```
5. Start the bot:
```
python CVEazy_main.py
```
### Mac/Linux Users:

1. Open Terminal.

2. Navigate to the bot folder:
```
cd path/to/CVEazy
```
4. Install required dependencies:
```
pip3 install -r requirements.txt
```
5. Start the bot:
```
python3 CVEazy_main.py
```

## 🛠️ Troubleshooting

### "Bot is running, but I don’t get messages!"

* Check that you entered the correct user ID in config.json.

* Make sure your bot is online in the Discord Developer Portal.

* Ensure your bot was actually added to your server, and its a server you own and have manage server permissions for.

### "Bot closes when I shut down my computer!"

* You will need to use a cloud server or a hosting service if you want it online 24/7.
