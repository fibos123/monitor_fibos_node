# FIBOS 节点状态监控器

[![GitHub Actions Workflow Status](https://github.com/fibos123/monitor_fibos_node/actions/workflows/monitor_fibos_node.yml/badge.svg)](https://github.com/fibos123/monitor_fibos_node/actions/workflows/monitor_fibos_node.yml)

这是一个使用 GitHub Actions 和 Python 实现的自动化监控项目，用于定期检查一个或多个指定的 FIBOS 区块链节点的状态。当发现有节点处于异常状态时，它会通过电子邮件发送一封格式可自定义的合并警报。

## ✨ 功能特性

- **多节点监控**: 可通过环境变量轻松配置，同时监控任意数量的节点。
- **自动化运行**: 无需服务器，完全基于免费的 GitHub Actions 定时执行。
- **精准警报**: 仅在节点的 `abnormal` 状态为 `true` 时发送通知。
- **合并通知**: 一次运行中若发现多个异常节点，将发送一封邮件汇总所有问题节点，避免邮件轰炸。
- **高度可定制的邮件通知**: 可自由修改邮件的发件人名称、主题和正文模板，并支持动态插入异常节点列表。
- **安全配置**: 所有敏感信息（如邮箱密码）均通过 GitHub **Repository Secrets** 安全存储。
- **现代化的本地开发**: 支持使用 `uv` 进行快速、简单的本地环境设置和测试。

---

## 🚀 如何工作

项目核心是一个 Python 脚本，由 GitHub Actions 调度执行。

1.  **定时触发**: Workflow 根据预设的 `cron` 表达式（默认每12小时）或手动触发来启动。
2.  **执行 Python 脚本**: GitHub Actions 环境会安装所需依赖并运行 `monitor_and_notify.py` 脚本。
3.  **获取并分析数据**: 脚本向 FIBOS 的 BP API (`https://bp.fibos.io/1.0/app/data/live`) 发送请求，获取所有节点的最新状态，并检查预设监控列表中的节点 `abnormal` 状态。
4.  **条件性发送邮件**: 如果发现任何异常节点，脚本会使用配置好的 SMTP 信息和邮件模板，发送一封包含所有异常节点名称的警报邮件。如果所有节点正常，则脚本会安静地退出。

---

## 🛠️ 远程部署与配置 (GitHub Actions)

请按照以下步骤来配置和启用此监控器。

### 步骤 1: 准备邮箱凭据 (以 Gmail 为例)

为了让 GitHub Actions 能发送邮件，您需要为您的邮箱账户生成一个**应用专用密码**。

1.  登录您的 Google 账户，前往 [Google 账户安全设置](https://myaccount.google.com/security)。
2.  确保您已启用“两步验证”。
3.  在“您登录 Google 的方式”部分，点击“应用专用密码”。
4.  选择应用为“邮件”，设备为“其他（自定义名称）”，输入 `GitHub Actions Monitor`，然后点击“生成”。
5.  Google 会生成一个 **16 位的密码**。请**立即复制并妥善保管**，此密码将用于下一步。

### 步骤 2: 配置 GitHub Repository Secrets

所有敏感信息都必须存储在 **Repository Secrets** 中，以确保安全。

1.  进入您的 GitHub 仓库，点击 **Settings** -> **Secrets and variables** -> **Actions**。
2.  在 **Repository secrets** 这个区域，点击 **New repository secret** 按钮。
3.  创建以下两个 Secrets：
    *   **`MAIL_USERNAME`**:
        *   值为您的完整 Gmail 地址（例如 `your.email@gmail.com`）。
    *   **`MAIL_PASSWORD`**:
        *   值为您在上一步中生成的 **16 位应用专用密码**。

### 步骤 3: 自定义 Workflow 配置

打开 `.github/workflows/monitor_fibos_node.yml` 文件，修改 `env` 部分以满足您的需求。

```yaml
env:
  # --- 基础配置 ---
  # !! 重要：将您要监控的节点名称填入此处，用逗号分隔，不要有空格
  NODE_NAMES: "fibos123comm,chainmoefibo"
  # !! 修改为您自己的收件人邮箱
  RECIPIENT_EMAIL: "bp@fibos123.com"
```

---

## 💻 本地开发与测试

本项目使用 [uv](https://github.com/astral-sh/uv) 进行现代、快速的 Python 包管理。

### 步骤 1: 安装 uv 和设置环境

1.  **安装 uv**: 如果你还没有安装 `uv`，请参照官方指南进行安装。对于 macOS 和 Linux：
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **克隆仓库**:
    ```bash
    git clone https://github.com/fibos123/monitor_fibos_node.git
    cd monitor_fibos_node
    ```

### 步骤 2: 配置本地变量

1.  **创建 `.env` 文件**: 从模板复制一份配置文件。此文件已被 `.gitignore` 忽略，不会被提交。
    ```bash
    cp .env.example .env
    ```
2.  **编辑 `.env` 文件**: 打开 `.env` 文件，填入你用于本地测试的真实信息（特别是 SMTP 相关的用户名和应用专用密码）。

### 步骤 3: 运行脚本

配置完成后，使用 `uv` 来运行监控脚本。`uv run` 会确保脚本在正确的虚拟环境中执行。

```bash
uv run monitor_and_notify.py
```

脚本将读取 `.env` 文件中的配置，执行与 GitHub Actions 中完全相同的检查和通知逻辑。

---

## 📝 许可证

本项目采用 [MIT License](LICENSE) 授权。