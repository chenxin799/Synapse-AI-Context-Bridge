# 🌉 Bridge (AI Context Manager)

**Bridge** 是一个专为 **"Human -> Web LLM -> AI Editor"** 工作流设计的上下文序列化工具。

它不仅仅是一个代码打包器，它是一个**协议转换器**。它将本地代码仓库转换为 LLM (如 Gemini, Claude, GPT-4) 能够理解的**架构师视图 (Symbol Map)**，并强制 LLM 输出 AI 编辑器 (如 Trae, Cursor) 能够直接执行的**施工指令 (Spec)**。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/UI-PyQt5-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## ✨ 核心特性 (Key Features)

* **🔍 符号地图 (Symbol Map)**: 自动提取类与函数摘要，让 LLM 瞬间理解项目骨架，不再盲读代码。
* **🎯 聚焦模式 (Focus Mode)**: 在 UI 树中勾选特定文件，即可忽略大小限制，精准修复 Bug。
* **📋 自动协议 (Auto-Protocol)**: 注入 `<trae_spec>` 系统指令，让 LLM 输出标准化的修改建议（@Filename, [Action], [Code]）。
* **🔒 安全剪贴板 (Secure Clipboard)**: 生成的内容自动写入剪贴板，并在 60 秒后自动销毁，防止代码泄露。
* **🎨 极简 UI (Minimalist UI)**: 基于 PyQt5 的现代化白色极简界面，支持全选/清空操作。

## 🚀 快速开始 (Quick Start)

### 1. 安装依赖
```bash
pip install -r requirements.txt
