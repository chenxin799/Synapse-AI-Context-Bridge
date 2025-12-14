<div align="center">
🧠 Synapse
连接人类意图与 AI 执行的神经突触
https://www.python.org/
https://riverbankcomputing.com/software/pyqt/
https://github.com/
LICENSE
http://makeapullrequest.com
功能特性 • 工作流 • 快速开始 • 贡献
</div>
📖 简介 (Introduction)
Synapse 是一个专为 "Human -> Web LLM -> AI Editor" 工作流设计的上下文序列化工具。
在 AI 辅助编程的时代，我们经常需要在 Web 端大模型（如 Gemini 1.5 Pro, GPT-4o, Claude 3.5）和本地 IDE（如 Trae, Cursor）之间反复横跳。
Synapse 解决了两个核心痛点：
让 Web LLM 瞬间看懂你的本地项目结构（Symbol Map）。
强制 LLM 输出 IDE 能 直接执行 的标准化施工指令（Spec）。
它不仅仅是一个代码备份器，它还是一个协议转换器。
📸 运行截图 (Screenshot)
<div align="center">
  <img src="screenshot.png" alt="Synapse UI Screenshot" width="800" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
  <br>
  <em>Synapse 的极简主义控制台界面</em>
</div>
✨ 核心特性 (Key Features)
表格
复制
特性	描述
🔍 符号映射
(Symbol Map)	自动提取 Class 与 Def 摘要，生成项目骨架地图，让 LLM 不再盲读海量代码，Token 节省 30%+。
🎯 聚焦模式
(Focus Mode)	在 UI 树中勾选特定文件，自动覆盖大小限制，实现对关键文件的“显微镜级”分析。
📋 自动协议
(Auto-Protocol)	内置 Prompt 注入系统，强制 LLM 输出 <trae_spec> 格式指令，包含 @Filename, [Action], [Code]。
🔒 安全剪贴板
(Secure)	生成的上下文自动写入系统剪贴板，并在 60 秒后自动销毁，防止敏感代码泄露。
🎨 极简 UI
(Minimalist)	基于 PyQt5 打造的现代化白色极简界面，支持文件全选/清空、状态实时监控。
🔄 工作流 (Workflow)
Synapse 在你的工作流中扮演“翻译官”的角色：
Mermaid
全屏 
下载 
复制
代码
预览
1. 勾选文件 & 描述需求
2. 生成 XML
3. 粘贴 (Ctrl+V)
4. 输出 Spec 指令
5. 投喂
6. 自动修改代码
👨‍💻 人类开发者
🧠 Synapse
📋 系统剪贴板
☁️ Web LLM(Gemini/GPT)
📝 施工单
🤖 AI 编辑器(Trae/Cursor)
📂 本地代码库
📂 项目结构 (Structure)
复制
Synapse/
├── synapse_ui.py      # 主程序入口 (GUI)
├── bridge.py          # 核心逻辑与协议层
├── requirements.txt   # 依赖清单
├── README.md          # 说明文档
└── .gitignore         # Git 忽略规则
🚀 快速开始 (Quick Start)
1. 安装依赖
确保你的电脑已安装 Python 3.8+。
bash
复制
pip install -r requirements.txt
2. 启动 Synapse
bash
复制
python synapse_ui.py
3. 使用技巧
全选/清空：使用列表上方的按钮快速管理文件选择。
强制读取：默认忽略 >50KB 的文件，但如果你手动勾选了该文件，Synapse 会强制读取它。
安全模式：复制完成后，你可以看到底部的倒计时条，60 秒后剪贴板会自动清空。
🤝 贡献 (Contributing)
欢迎提交 Issue 或 Pull Request！
Fork 本仓库
创建特性分支 (git checkout -b feature/AmazingFeature)
提交更改 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
开启 Pull Request
📄 许可证 (License)
本项目采用 MIT License 开源。
