import sys
import os
import datetime
import subprocess
import re
import fnmatch

# --- PyQt5 导入 ---
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QTreeWidget, QTreeWidgetItem, QSplitter,
                             QFileDialog, QProgressBar, QHeaderView, QTreeWidgetItemIterator, QStyle, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon

# ==========================================
# 核心逻辑 (Core Logic) - 保持不变
# ==========================================
DEFAULT_IGNORE = [
    '.git', '.idea', '.vscode', '__pycache__', 'node_modules', 
    'venv', 'env', '.DS_Store', '*.pyc', '*.o', '*.png', '*.jpg', '*.dll', '*.exe',
    'bridge_ui.py', 'bridge.py', 'llm_context.xml', 'README.md', 'LICENSE'
]
MAX_FILE_SIZE = 50 * 1024

class CoreBridge:
    def __init__(self, root_dir, focus_files=None):
        self.root_dir = root_dir
        self.focus_files = focus_files
        self.ignore_patterns = DEFAULT_IGNORE.copy()
        self.load_gitignore()

    def load_gitignore(self):
        gitignore_path = os.path.join(self.root_dir, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'): self.ignore_patterns.append(line)

    def is_ignored(self, path):
        name = os.path.basename(path)
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(name, pattern): return True
            if pattern.endswith('/') and name == pattern.rstrip('/'): return True
        return False

    def generate_symbol_map(self, file_content, file_path):
        symbols = []
        if file_path.endswith('.py'):
            lines = file_content.split('\n')
            for i, line in enumerate(lines):
                if re.match(r'^\s*(class|def)\s+', line):
                    symbols.append(f"Line {i+1}: {line.strip().rstrip(':')}")
        return "\n".join(symbols) if symbols else "No symbols detected."

    def scan_files(self):
        file_blocks = []
        symbol_maps = []
        
        target_files = []
        if self.focus_files:
            for rel_path in self.focus_files:
                abs_path = os.path.join(self.root_dir, rel_path)
                if os.path.exists(abs_path):
                    target_files.append(abs_path)
        else:
            for root, dirs, files in os.walk(self.root_dir):
                dirs[:] = [d for d in dirs if not self.is_ignored(os.path.join(root, d))]
                for f in files:
                    full_p = os.path.join(root, f)
                    if not self.is_ignored(full_p):
                        target_files.append(full_p)

        for file_path in target_files:
            rel_path = os.path.relpath(file_path, self.root_dir)
            try:
                file_size = os.path.getsize(file_path)
                is_forced = bool(self.focus_files) and (rel_path in self.focus_files)
                
                if file_size > MAX_FILE_SIZE and not is_forced:
                    content = f"// [Bridge] 文件过大 ({file_size/1024:.1f}KB) 已跳过. 请在左侧勾选以强制读取."
                    raw_content = ""
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                        lines = raw_content.split('\n')
                        content = "\n".join([f"{i+1:4} | {line}" for i, line in enumerate(lines)])

                if raw_content:
                    s_map = self.generate_symbol_map(raw_content, rel_path)
                    symbol_maps.append(f"File: {rel_path}\n{s_map}\n" + "-"*30)

                file_blocks.append(f'    <file path="{rel_path}">\n<![CDATA[\n{content}\n]]>\n    </file>')
            except Exception: pass

        return '\n'.join(symbol_maps), '\n'.join(file_blocks)

# ==========================================
# UI 界面代码 (Bridge v1.3 - 布局优化版)
# ==========================================
class BridgeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bridge")
        self.resize(1000, 720) # 稍微增加高度
        self.root_dir = os.getcwd()
        self.core_bridge = CoreBridge(self.root_dir)
        self.timer_val = 60
        
        self.init_ui()
        self.apply_styles()
        self.refresh_file_tree()

    def apply_styles(self):
        # 极简白风格 CSS
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #212529; font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif; font-size: 10pt;
            }
            QLabel { 
                color: #495057; font-weight: 600; margin-bottom: 2px;
            }
            QLineEdit, QTextEdit {
                background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 8px; color: #212529;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #007aff; background-color: #ffffff;
            }
            QLineEdit[readOnly="true"] { color: #6c757d; background-color: #e9ecef; }
            QTreeWidget {
                background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 6px;
            }
            QTreeWidget::item { padding: 6px; }
            QTreeWidget::item:hover { background-color: #f1f3f5; }
            QTreeWidget::item:selected, QTreeWidget::item:selected:active {
                background-color: #e7f5ff; color: #007aff;
            }
            QHeaderView::section {
                background-color: #f8f9fa; border: none; border-bottom: 2px solid #dee2e6; padding: 6px; font-weight: bold; color: #495057;
            }
            QSplitter::handle { background-color: #e9ecef; }
            
            /* 按钮样式优化 */
            QPushButton {
                background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px;
                padding: 6px 12px; color: #495057; font-weight: 600;
            }
            QPushButton:hover { background-color: #e2e6ea; border-color: #dae0e5; color: #212529; }
            
            /* 操作按钮组 (全选/清空) */
            QPushButton.ToolBtn {
                background-color: #ffffff; border: 1px solid #ced4da; font-size: 9pt; padding: 4px 8px;
            }
            QPushButton.ToolBtn:hover { background-color: #f1f3f5; color: #007aff; border-color: #007aff; }
            
            /* 主行动按钮 */
            QPushButton#ActionBtn {
                background-color: #007aff; color: white; border: none; font-size: 11pt; padding: 10px 20px;
            }
            QPushButton#ActionBtn:hover { background-color: #0069d9; }
            
            QProgressBar {
                border: none; background-color: #e9ecef; border-radius: 4px;
                text-align: center; color: #6c757d; font-size: 9pt; font-weight: bold;
            }
            QProgressBar::chunk { background-color: #007aff; border-radius: 4px; }
            QTextEdit#LogOutput { font-family: 'Consolas', monospace; font-size: 9pt; background-color: #f8f9fa; color: #343a40; }
        """)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(24, 24, 24, 24) # 增加外边距
        layout.setSpacing(18) # 增加控件间距

        # --- 顶部：路径选择 (优化布局) ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)
        
        lbl_root = QLabel("项目根目录:")
        lbl_root.setMinimumWidth(80) # 防止文字被挤压
        
        self.path_input = QLineEdit(self.root_dir)
        self.path_input.setReadOnly(True)
        self.path_input.setMinimumWidth(300)
        
        btn_browse = QPushButton("切换项目")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.clicked.connect(self.browse_folder)
        
        top_layout.addWidget(lbl_root)
        top_layout.addWidget(self.path_input)
        top_layout.addWidget(btn_browse)
        layout.addLayout(top_layout)

        # --- 中部：左右分栏 ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        
        # === 左侧：文件树区域 (布局重构) ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 12, 0) # 右侧留白
        left_layout.setSpacing(8)
        
        # 1. 标题行
        left_layout.addWidget(QLabel("源文件列表 (勾选以聚焦)"))
        
        # 2. 工具按钮行 (新的一行，防止拥挤)
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(8)
        
        btn_select_all = QPushButton("全选")
        btn_select_all.setProperty("class", "ToolBtn") # 应用特定样式
        btn_select_all.clicked.connect(self.select_all_items)
        
        btn_clear_all = QPushButton("清空")
        btn_clear_all.setProperty("class", "ToolBtn")
        btn_clear_all.clicked.connect(self.clear_all_items)
        
        tools_layout.addWidget(btn_select_all)
        tools_layout.addWidget(btn_clear_all)
        left_layout.addLayout(tools_layout)
        
        # 3. 文件树
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("文件名")
        self.tree_widget.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree_widget.itemChanged.connect(self.on_tree_item_changed)
        left_layout.addWidget(self.tree_widget)
        
        splitter.addWidget(left_widget)

        # === 右侧：输入与日志区域 ===
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(12, 0, 0, 0) # 左侧留白
        right_layout.setSpacing(10)
        
        right_layout.addWidget(QLabel("架构师指令 (描述需求)"))
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("在此输入你的需求...\n例如：'帮我分析 main.py 中的死锁问题，并给出修复方案'")
        self.query_input.setMaximumHeight(120)
        right_layout.addWidget(self.query_input)
        
        right_layout.addWidget(QLabel("运行日志"))
        self.log_output = QTextEdit()
        self.log_output.setObjectName("LogOutput")
        self.log_output.setReadOnly(True)
        right_layout.addWidget(self.log_output)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3) # 左侧比例
        splitter.setStretchFactor(1, 5) # 右侧比例
        layout.addWidget(splitter)

        # --- 底部：操作栏 ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)
        
        self.status_bar = QProgressBar()
        self.status_bar.setRange(0, 60)
        self.status_bar.setValue(0)
        self.status_bar.setFormat("系统就绪")
        self.status_bar.setFixedHeight(35) # 加高进度条
        
        self.btn_run = QPushButton("⚡ 生成数据包并复制")
        self.btn_run.setObjectName("ActionBtn")
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.setFixedHeight(40) # 加高按钮
        self.btn_run.clicked.connect(self.run_bridge)
        
        bottom_layout.addWidget(self.status_bar, stretch=3)
        bottom_layout.addWidget(self.btn_run, stretch=2)
        layout.addLayout(bottom_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clipboard_timer)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择项目根目录", self.root_dir)
        if folder:
            self.root_dir = folder
            self.path_input.setText(folder)
            self.core_bridge = CoreBridge(folder)
            self.refresh_file_tree()
            self.log(f"项目上下文已切换至: {folder}")

    def refresh_file_tree(self):
        self.tree_widget.clear()
        self.tree_widget.itemChanged.disconnect(self.on_tree_item_changed)
        
        root_item = QTreeWidgetItem(self.tree_widget, [os.path.basename(self.root_dir)])
        root_item.setExpanded(True)
        root_item.setIcon(0, QApplication.style().standardIcon(QStyle.SP_DirIcon))
        self._add_tree_items(self.root_dir, root_item)
        
        self.tree_widget.itemChanged.connect(self.on_tree_item_changed)

    def _add_tree_items(self, current_path, parent_item):
        try:
            items = os.listdir(current_path)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower()))
            for item in items:
                full_path = os.path.join(current_path, item)
                if self.core_bridge.is_ignored(full_path): continue
                tree_item = QTreeWidgetItem(parent_item, [item])
                tree_item.setData(0, Qt.UserRole, full_path)
                tree_item.setCheckState(0, Qt.Unchecked)
                if os.path.isdir(full_path):
                    tree_item.setIcon(0, QApplication.style().standardIcon(QStyle.SP_DirIcon))
                    self._add_tree_items(full_path, tree_item)
                else:
                    tree_item.setIcon(0, QApplication.style().standardIcon(QStyle.SP_FileIcon))
        except PermissionError: pass

    def select_all_items(self):
        self._set_all_check_state(Qt.Checked)
        self.log("已全选所有文件")

    def clear_all_items(self):
        self._set_all_check_state(Qt.Unchecked)
        self.log("已清空选择")

    def _set_all_check_state(self, state):
        self.tree_widget.itemChanged.disconnect(self.on_tree_item_changed)
        iterator = QTreeWidgetItemIterator(self.tree_widget)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, state)
            iterator += 1
        self.tree_widget.itemChanged.connect(self.on_tree_item_changed)

    def on_tree_item_changed(self, item, column):
        pass

    def get_checked_files(self):
        checked_files = []
        iterator = QTreeWidgetItemIterator(self.tree_widget, QTreeWidgetItemIterator.Checked)
        while iterator.value():
            item = iterator.value()
            full_path = item.data(0, Qt.UserRole)
            if full_path and os.path.isfile(full_path):
                rel = os.path.relpath(full_path, self.root_dir)
                checked_files.append(rel)
            iterator += 1
        return checked_files

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def run_bridge(self):
        query = self.query_input.toPlainText().strip()
        focus_files = self.get_checked_files()
        
        self.log("正在打包项目上下文...")
        if focus_files:
            self.log(f"-> 模式: 聚焦模式 (已选中 {len(focus_files)} 个文件)")
        else:
            self.log("-> 模式: 全量扫描 (已应用大小限制)")

        self.core_bridge.focus_files = focus_files
        self.core_bridge.user_query = query
        
        try:
            s_maps, f_contents = self.core_bridge.scan_files()
            protocol_prompt = """
Communication Rules (双向沟通协议):
1. Read <symbol_map> for overview (先读符号地图).
2. Analyze <project_files> with line numbers (再分析具体代码).
3. Output strictly in <trae_spec> format (严格按照以下格式输出):
   @Filename
   [Context] (Simple explanation why)
   [Action] (Refactor/Add/Fix)
   [Code] (The code snippet)
"""
            final_xml = f"""<project_context>
    <meta><timestamp>{datetime.datetime.now()}</timestamp></meta>
    {protocol_prompt}
    <symbol_map>\n{s_maps}\n    </symbol_map>
    <project_files>\n{f_contents}\n    </project_files>
    <user_query>\n        {query}\n    </user_query>
</project_context>"""

            clipboard = QApplication.clipboard()
            clipboard.setText(final_xml)
            
            self.log(f"✅ 成功! 数据包 ({len(final_xml)/1024:.2f} KB) 已复制到剪贴板。")
            self.log("👉 请直接去网页版 LLM 粘贴 (Ctrl+V)")
            
            self.timer_val = 60
            self.timer.start(1000)
            self.status_bar.setValue(60)
            self.status_bar.setStyleSheet("QProgressBar::chunk { background-color: #007aff; }")
            
        except Exception as e:
            self.log(f"❌ 错误: {str(e)}")
            QMessageBox.critical(self, "生成错误", str(e))

    def update_clipboard_timer(self):
        self.timer_val -= 1
        self.status_bar.setValue(self.timer_val)
        self.status_bar.setFormat(f"剪贴板将在 {self.timer_val}秒 后自动销毁")
        if self.timer_val <= 0:
            self.timer.stop()
            clipboard = QApplication.clipboard()
            clipboard.clear()
            self.status_bar.setFormat("剪贴板已清空 (安全)")
            self.status_bar.setStyleSheet("QProgressBar::chunk { background-color: #dc3545; }")
            self.log("🔒 剪贴板数据已自动销毁。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Microsoft YaHei", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    window = BridgeWindow()
    window.show()
    sys.exit(app.exec_())