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
- 修改/维护：[Andrew/Andrewww1228]
