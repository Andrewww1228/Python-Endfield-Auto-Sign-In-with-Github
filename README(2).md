# Endfield Auto Sign-in 🚀

An automated daily check-in script for **Arknights: Endfield** (Skland/Skport) using GitHub Actions. It handles daily sign-ins for both CN and Global servers and sends a summary notification to a Discord Webhook.

## ✨ Features
- **Automation:** Runs daily at 00:30 UTC (08:30 AM Malaysia Time).
- **Multi-Account Support:** Supports multiple tokens separated by a semicolon (`;`).
- **Discord Integration:** Sends beautiful embed notifications with success/failure status.
- **Anti-Ban:** Includes randomized delays and varied User-Agents to mimic real app behavior.

## 🛠️ Setup Instructions

### 1. Fork this Repository
Click the **Fork** button at the top right of this page to create your own copy.

### 2. Configure GitHub Secrets
Go to your forked repository's **Settings > Secrets and variables > Actions** and add the following **New repository secrets**:

| Secret Name | Description |
| :--- | :--- |
| `SKYLAND_TOKEN` | Your Skland token for the CN server (optional). |
| `SKPORT_TOKEN` | Your Skport token for the Global server (optional). |
| `DISCORD_WEBHOOK` | Your Discord Webhook URL for notifications. |

> ⚠️ **Important Security Note:** If you decide to put your account token directly inside the Python file instead of using GitHub Secrets, you **MUST** make your repository **Private**. 

### 🔑 How to Extract your Token
1. Log in to your **SKPORT/Skland** account through your web browser.
2. Open a new tab and go to: [https://web-api.skport.com/cookie_store/account_token](https://web-api.skport.com/cookie_store/account_token)
3. Copy the value inside `"data": {"content": "YOUR_TOKEN_HERE"}`.
4. This is the value you paste into your GitHub Secrets.

### 3. Enable GitHub Actions
Go to the **Actions** tab of your repo and click "I understand my workflows, go ahead and enable them."

## 📝 Configuration
The script is configured to run automatically. To run it manually:
1. Go to the **Actions** tab.
2. Select **Endfield Auto Sign**.
3. Click **Run workflow**.

## 🛡️ Disclaimer
This script is for educational purposes only. Use it at your own risk. The author is not responsible for any account issues related to the use of this automation.

## 👤 Credits
- Script Logic: Based on `sjtt2`
- https://github.com/sjtt2/endfield_auto_sign
- Modified by: [Andrew/Andrewww1228]
