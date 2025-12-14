# 🧠 Synapse

**连接人类意图与 AI 执行的神经突触**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![Protocol](https://img.shields.io/badge/Protocol-Trae%20Spec-FF6B6B?style=flat-square)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

[功能特性](#-核心特性-key-features) • [工作流](#-工作流-workflow) • [快速开始](#-快速开始-quick-start) • [贡献](#-贡献-contributing)

---

## 📖 简介 (Introduction)

**Synapse** 是一个专为 **"Human -> Web LLM -> AI Editor"** 工作流设计的上下文序列化工具。

在 AI 辅助编程的时代，我们经常需要在 Web 端大模型（如 Gemini 1.5 Pro, GPT-4o, Claude 3.5）和本地 IDE（如 Trae, Cursor）之间反复横跳。

**Synapse 解决了两个核心痛点：**

1. 让 Web LLM **瞬间看懂**你的本地项目结构（Symbol Map）。
2. 强制 LLM 输出 IDE 能 **直接执行** 的标准化施工指令（Spec）。

它不仅仅是一个代码备份器，它还是一个**协议转换器**。

## 📸 运行截图 (Screenshot)

<div align="center">
  <img src="screenshot.png" alt="Synapse UI Screenshot" width="800" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
  <br>
  <em style="display: block; margin-top: 8px;">Synapse 的极简主义控制台界面</em>
</div>

## ✨ 核心特性 (Key Features)

| 特性 | 描述 |
| :--- | :--- |
| **🔍 符号映射**<br>*(Symbol Map)* | 自动提取 Class 与 Def 摘要，生成项目骨架地图，让 LLM 不再盲读海量代码，**Token 节省 30%+**。 |
| **🎯 聚焦模式**<br>*(Focus Mode)* | 在 UI 树中勾选特定文件，自动覆盖大小限制，实现对关键文件的**“显微镜级”分析**。 |
| **📋 自动协议**<br>*(Auto-Protocol)* | 内置 Prompt 注入系统，强制 LLM 输出 `<trae_spec>` 格式指令，包含 `@Filename`, `[Action]`, `[Code]`。 |
| **🔒 安全剪贴板**<br>*(Secure)* | 生成的上下文自动写入系统剪贴板，并在 **60 秒后自动销毁**，防止敏感代码泄露。 |
| **🎨 极简 UI**<br>*(Minimalist)* | 基于 PyQt5 打造的现代化白色极简界面，支持文件全选/清空、状态实时监控。 |

## 🔄 工作流 (Workflow)

Synapse 在你的工作流中扮演**“翻译官”**的角色：

```mermaid
graph LR
    A["👨‍💻 人类开发者"] -->|"1. 勾选文件 & 描述需求"| B("🧠 Synapse")
    B -->|"2. 生成 XML"| C{"📋 系统剪贴板"}
    C -->|"3. 粘贴 (Ctrl+V)"| D["☁️ Web LLM (Gemini/GPT)"]
    D -->|"4. 输出 Spec 指令"| E["📝 施工单"]
    E -->|"5. 投喂"| F["🤖 AI 编辑器 (Trae/Cursor)"]
    F -->|"6. 自动修改代码"| G["📂 本地代码库"]
```

## 📂 项目结构 (Structure)

```plaintext
Synapse/
├── synapse_ui.py      # 主程序入口 (GUI)
├── bridge.py          # 核心逻辑与协议层
├── requirements.txt   # 依赖清单
├── README.md          # 说明文档
└── .gitignore         # Git 忽略规则
```

## 🚀 快速开始 (Quick Start)

### 1. 安装依赖

确保你的电脑已安装 Python 3.8+。

```bash
pip install -r requirements.txt
```

### 2. 启动 Synapse

```bash
python synapse_ui.py
```

### 3. 使用技巧

- **全选/清空**：使用列表上方的按钮快速管理文件选择。
- **强制读取**：默认忽略 >50KB 的文件，但如果你手动勾选了该文件，Synapse 会强制读取它。
- **安全模式**：复制完成后，你可以看到底部的倒计时条，60秒后剪贴板会自动清空。

## 🤝 贡献 (Contributing)

欢迎提交 Issue 或 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证 (License)

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源。
