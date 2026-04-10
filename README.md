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

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 终末地自动签到脚本 🚀

一个基于 GitHub Actions 的 **《明日方舟：终末地》** (森空岛 Skland/Skport) 自动签到脚本。支持国服与国际服双向签到，并通过 Discord Webhook 发送详细的签到结果通知。

## ✨ 功能特点
- **完全自动化：** 每日 UTC 00:30 (马来西亚/北京时间 08:30 AM) 自动运行。
- **多账号支持：** 支持配置多个 Token，使用英文分号 (`;`) 分隔即可。
- **Discord 推送：** 签到成功、重复或失败均有精美的卡片推送。
- **防封号设计：** 内置随机延迟和多种 User-Agent 模拟真实 App 行为。

## 🛠️ 设置指南

### 1. Fork 本仓库
点击页面右上角的 **Fork** 按钮，将项目克隆到你自己的账号下。

### 2. 配置 GitHub Secrets
进入你 Fork 后的仓库，点击 **Settings > Secrets and variables > Actions**，添加以下 **New repository secrets**:

| 变量名 (Secret Name) | 描述 |
| :--- | :--- |
| `SKYLAND_TOKEN` | 森空岛 (国服) 账号 Token (可选)。 |
| `SKPORT_TOKEN` | Skport (国际服) 账号 Token (可选)。 |
| `DISCORD_WEBHOOK` | Discord Webhook 链接，用于接收通知。 |

> ⚠️ **重要安全提示：** 如果你选择直接将 Token 写在 Python 文件中而不是使用 GitHub Secrets，请务必将你的仓库设置为 **私有 (Private)**。

### 🔑 如何获取你的 Token
1. 在浏览器中登录你的 **SKPORT (国际服)** 或 **森空岛 (国服)** 账号。
2. 打开一个新标签页，访问：[https://web-api.skport.com/cookie_store/account_token](https://web-api.skport.com/cookie_store/account_token)
3. 复制 `"data": {"content": "这里是你的 TOKEN"}` 括号中的内容。
4. 将该内容粘贴到 GitHub Secrets 对应的变量中。

### 3. 开启 GitHub Actions
点击仓库顶部的 **Actions** 选项卡，点击 "I understand my workflows, go ahead and enable them" 以激活自动化任务。

## 📝 手动触发
脚本默认定时运行。如果你想立即测试：
1. 点击 **Actions** 选项卡。
2. 在左侧选择 **Endfield Auto Sign**。
3. 点击 **Run workflow** 手动执行。

## 🛡️ 免责声明
本脚本仅用于学习交流。请自行承担使用风险，作者不对任何因自动化脚本引起的账号问题负责。

## 👤 致谢
- 核心逻辑：基于 `sjtt2` 的开源方案
- https://github.com/sjtt2/endfield_auto_sign
- 修改/维护：[Andrew/Andrewww1228]
