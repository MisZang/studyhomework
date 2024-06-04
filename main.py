import sys
# 导入Tkinter库，用于创建图形用户界面
import tkinter as tk
# 导入ttk模块，提供更现代的控件样式
from tkinter import ttk
# 导入学生信息标签页模块
from student_info import StudentInfoTab
# 导入查找学生标签页模块
from search_student import SearchStudentTab
# 导入所有学生标签页模块
from all_students import AllStudentsTab
# 导入子进程模块，用于执行外部命令
import subprocess
# 导入系统模块，用于访问解释器路径等系统特定参数

# 定义一个函数，用于检查并安装所需的Python包
def check_and_install_packages():
    # 定义一个列表，存储需要检查的包名称
    required_packages = ["tkinter", "pandas", "matplotlib", "openpyxl"]
    # 循环遍历包列表
    for package in required_packages:
        try:
            # 尝试导入每个包，如果包已安装则跳过安装步骤
            if package == "pandas":
                import pandas
            elif package == "tkinter":
                import tkinter
            elif package == "matplotlib":
                import matplotlib
            elif package == "openpyxl":
                import openpyxl
            elif package == "sqlite3":
                import sqlite3
        except ImportError:
            # 如果包未安装，使用subprocess模块调用pip命令进行安装
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, '-i https://mirrors.aliyun.com/pypi/simple/'])

# 定义一个函数，用于设置窗口的4:3宽高比
def set_4_3_aspect_ratio(root):
    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 计算目标宽度和高度，初始设定为屏幕宽度和高度的一半
    target_width = int(screen_width * 0.5)
    target_height = int(screen_height * 0.5)

    # 如果目标高度大于屏幕高度，调整宽度和高度以符合屏幕高度
    if target_height > screen_height:
        target_height = screen_height
        target_width = int(screen_height / 3 * 4)

    # 设置窗口的大小
    root.geometry(f"{target_width}x{target_height}")

# 定义一个函数，用于调整DPI设置，以支持高分辨率屏幕
def adjust_dpi(root):
    try:
        # 尝试导入ctypes库，用于调用Windows API
        from ctypes import windll
        # 调用SetProcessDpiAwareness函数，使程序对高DPI屏幕友好
        windll.shcore.SetProcessDpiAwareness(1)
    except ImportError:
        # 如果ctypes库不可用或在非Windows系统上，不执行任何操作
        pass

# 定义主程序入口函数
def main():
    # 在其他代码执行前调用check_and_install_packages函数，确保所有必需的包已安装
    check_and_install_packages()
    # 创建Tkinter的主窗口对象
    root = tk.Tk()
    # 调整DPI设置
    adjust_dpi(root)
    # 设置窗口的4:3宽高比
    set_4_3_aspect_ratio(root)
    # 实例化学生管理系统类
    app = StudentManagementSystem(root)
    # 进入主事件循环
    root.mainloop()

# 定义学生管理系统类
class StudentManagementSystem:
    # 初始化方法，创建主窗口并设置标题
    def __init__(self, root):
        self.root = root
        self.root.title("简单学生管理系统")
        # 初始化学生数据列表
        self.students_data = []
        # 创建界面小部件
        self.create_widgets()
        # 绑定事件
        self.bind_events()

    # 创建界面小部件的方法
    def create_widgets(self):
        # 创建一个Notebook控件，用于管理多个标签页
        notebook = ttk.Notebook(self.root)
        # 将Notebook控件放置在主窗口中，填充整个空间
        notebook.pack(expand=1, fill='both')

        # 实例化所有学生标签页，并传入Notebook和学生数据列表
        self.all_students_tab = AllStudentsTab(notebook, self.students_data)
        # 实例化学生信息标签页，并传入Notebook、学生数据列表和所有学生标签页
        self.student_info_tab = StudentInfoTab(notebook, self.students_data, self.all_students_tab)
        # 实例化查找学生标签页，并传入Notebook和学生数据列表
        self.search_student_tab = SearchStudentTab(notebook, self.students_data)

        # 添加标签页到Notebook控件
        notebook.add(self.student_info_tab.frame, text='学生信息')
        notebook.add(self.search_student_tab.frame, text='查看学生')
        notebook.add(self.all_students_tab.frame, text='全部学生')

    # 绑定事件的方法
    def bind_events(self):
        # 绑定Ctrl + 鼠标滚轮事件到zoom方法
        self.root.bind("<Control-MouseWheel>", self.zoom)
        # 绑定Ctrl + 加号事件到zoom_in方法
        self.root.bind("<Control-plus>", self.zoom_in)
        # 绑定Ctrl + 减号事件到zoom_out方法
        self.root.bind("<Control-minus>", self.zoom_out)

    # 鼠标滚轮缩放事件处理方法
    def zoom(self, event):
        # 根据鼠标滚轮方向调用zoom_in或zoom_out方法
        if event.delta > 0:
            self.zoom_in(event)
        else:
            self.zoom_out(event)

    # 放大事件处理方法
    def zoom_in(self, event=None):
        # 获取当前窗口的宽度和高度
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        # 放大窗口，宽度和高度增加10%
        self.root.geometry(f"{int(width * 1.1)}x{int(height * 1.1)}")

    # 缩小事件处理方法
    def zoom_out(self, event=None):
        # 获取当前窗口的宽度和高度
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        # 缩小窗口，宽度和高度减少10%
        self.root.geometry(f"{int(width * 0.9)}x{int(height * 0.9)}")

# 如果脚本被直接运行（而非被导入），则调用main函数
if __name__ == "__main__":
    main()