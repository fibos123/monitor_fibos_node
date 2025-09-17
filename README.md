# FIBOS 出块节点状态监控器 ⚡️

[![GitHub Actions Workflow Status](https://github.com/fibos123/monitor_fibos_node/actions/workflows/monitor_fibos_node.yml/badge.svg)](https://github.com/fibos123/monitor_fibos_node/actions/workflows/monitor_fibos_node.yml)

一个轻量、自动化的 FIBOS 出块节点监控工具。它基于 **GitHub Actions** 运行，无需任何服务器，当检测到你关注的出块节点状态异常时，会自动发送一封汇总邮件提醒。

## ✨ 特性

- **多节点监控**: 在环境变量中轻松配置。
- **完全自动化**: 由 GitHub Actions 定时驱动，完全免费。
- **智能警报**: 仅在节点异常时发送通知，无异常不打扰。
- **邮件合并**: 一封邮件汇总所有异常节点，避免信息轰炸。
- **高度定制**: 邮件主题、内容、发件人等均可自定义。
- **绝对安全**: 邮箱密码等敏感信息通过 GitHub Secrets 安全存储。

---

## 🚀 三步完成配置

### 步骤 1: 创建邮箱应用密码

为了通过程序发送邮件，你需要一个**应用专用密码**（而不是你的登录密码）。

以 Gmail 为例：
1.  前往 [Google 账户安全设置](https://myaccount.google.com/security)。
2.  确保已开启 **两步验证**。
3.  点击 **应用专用密码**，生成一个 16 位的密码并复制它。

### 步骤 2: 设置 GitHub Secrets

在你的 GitHub 仓库中，前往 `Settings` > `Secrets and variables` > `Actions`，添加以下两个 **Repository secrets**：

- **`MAIL_USERNAME`**: 你的邮箱地址 (例如: `your.email@gmail.com`)。
- **`MAIL_PASSWORD`**: 你在上一步生成的 **16 位应用专用密码**。

### 步骤 3: 修改 Workflow 配置

打开 `.github/workflows/monitor_fibos_node.yml` 文件，修改 `env` 部分：

```yaml
env:
  # ⬇️ 替换成你要监控的节点名，用逗号分隔
  NODE_NAMES: "fibos123comm,chainmoefibo"
  
  # ⬇️ 替换成接收警报的邮箱
  RECIPIENT_EMAIL: "bp@fibos123.com"
```

**完成！** 提交你的修改，监控将自动按计划（默认每 12 小时）运行。

---

## ▶️ 如何运行

- **自动运行**: 推送代码到 `main` 分支后，监控将按 `cron` 计划自动执行。
- **手动触发**: 在仓库的 **Actions** 标签页，选择 "Monitor FIBOS Node Status"，点击 "Run workflow" 即可立即执行一次检查。

<br>

<details>
<summary><strong>💻 本地开发与测试</strong></summary>

本项目使用 [uv](https://github.com/astral-sh/uv) 进行快速包管理。

1.  **安装 uv** (macOS/Linux):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **克隆仓库并进入目录**:
    ```bash
    git clone https://github.com/fibos123/monitor_fibos_node.git
    cd monitor_fibos_node
    ```
3.  **配置本地环境变量**:
    ```bash
    cp .env.example .env
    # 编辑 .env 文件，填入你的 SMTP 和测试信息
    ```
4.  **运行脚本**:
    ```bash
    uv run monitor_and_notify.py
    ```
</details>

---

## 📝 许可证

[MIT License](LICENSE)
