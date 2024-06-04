# 导入Tkinter库，这是Python的标准GUI库
import tkinter as tk
# 导入Tkinter的子库ttk，用于现代风格的小部件
from tkinter import ttk
# 导入文件对话框模块，用于文件选择对话框
from tkinter import filedialog
# 导入消息框模块，用于显示警告、错误和信息对话框
from tkinter import messagebox
# 导入Pandas库，用于数据处理和分析
import pandas as pd
# 导入SQLite3库，用于轻量级的数据库操作
import sqlite3
# 导入操作系统库，用于文件路径操作
import os

# 定义AllStudentsTab类，用于管理所有学生的标签页
class AllStudentsTab:
    # 初始化方法，创建标签页的框架和数据结构
    def __init__(self, notebook, students_data):
        self.frame = ttk.Frame(notebook)  # 创建一个ttk框架作为标签页的内容区域
        self.students_data = students_data  # 保存学生数据
        self.current_file_path = None  # 当前文件路径，初始化为空
        self.create_widgets()  # 调用create_widgets方法创建小部件
        self.load_recent_excel()  # 加载最近使用的Excel文件

    # 创建小部件方法，用于构建界面元素
    def create_widgets(self):
        # 定义树状视图的列名
        columns = [
            "院系", "专业", "班级", "学号", "姓名", "年龄",
            "出生日期", "性别", "科目1", "科目2", "科目3",
            "科目4", "科目5", "最高分", "最低分", "平均分",
            "总分", "备注"
        ]
        
        # 创建树状视图的框架
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.pack(expand=1, fill='both')  # 填充整个框架区域
        
        # 创建树状视图，用于展示学生数据
        self.student_tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        
        # 遍历列名，设置列标题和宽度
        for col in columns:
            self.student_tree.heading(col, text=col)  # 设置列标题
            self.student_tree.column(col, width=100)  # 设置列宽
        
        # 创建垂直滚动条
        self.v_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        # 创建水平滚动条
        self.h_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.student_tree.xview)
        
        # 将滚动条与树状视图关联
        self.student_tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        # 布局滚动条
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.student_tree.pack(expand=1, fill='both')  # 布局树状视图
        
        # 刷新树状视图，加载学生数据
        self.refresh_treeview()
        
        # 创建按钮框架
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)  # 按钮框架与上方的间距
        
        # 创建并布局按钮
        ttk.Button(button_frame, text="导出为Excel", command=self.export_to_excel).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="导入Excel", command=self.import_from_excel).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="导出到数据库", command=self.export_to_database).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="从数据库导入", command=self.import_from_database).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="工作模式", command=self.ai_suggestions).pack(side='left', padx=5, pady=5)

    # 刷新树状视图方法，更新学生数据
    def refresh_treeview(self):
        # 清空树状视图
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        # 遍历学生数据，插入到树状视图中
        for student in self.students_data:
            self.student_tree.insert('', tk.END, values=[student[col] for col in self.student_tree['columns']])

    # 导出数据到Excel文件方法
    def export_to_excel(self):
        # 弹出文件保存对话框，获取文件路径
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            # 获取列名
            columns = [self.student_tree.heading(col)["text"] for col in self.student_tree["columns"]]
            # 获取数据，转换为DataFrame
            data = [self.student_tree.item(child)["values"] for child in self.student_tree.get_children()]
            df = pd.DataFrame(data, columns=columns)
            # 导出数据到Excel文件
            df.to_excel(file_path, index=False)
            self.current_file_path = file_path  # 更新当前文件路径
            self.save_recent_file_path(file_path)  # 保存最近文件路径
            messagebox.showinfo("提示", "导出为Excel成功")  # 显示导出成功的消息框

    # 导入数据从Excel文件方法
    def import_from_excel(self):
        # 弹出文件打开对话框，获取文件路径
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            # 加载Excel文件
            self.load_excel(file_path)
            self.save_recent_file_path(file_path)  # 保存最近文件路径

    # 加载Excel文件数据方法
    def load_excel(self, file_path):
        # 使用Pandas读取Excel文件
        df = pd.read_excel(file_path)
        # 清空学生数据列表
        self.students_data.clear()
        # 遍历DataFrame，将数据转换为字典并添加到学生数据列表中
        for _, row in df.iterrows():
            self.students_data.append(row.to_dict())
        # 刷新树状视图
        self.refresh_treeview()
        self.current_file_path = file_path  # 更新当前文件路径
        messagebox.showinfo("提示", "导入Excel成功")  # 显示导入成功的消息框

    # 加载最近使用的Excel文件方法
    def load_recent_excel(self):
        # 读取最近使用的文件路径
        recent_file_path = self.get_recent_file_path()
        if recent_file_path and os.path.exists(recent_file_path):  # 如果文件路径存在
            # 加载Excel文件
            self.load_excel(recent_file_path)

    # 保存最近使用的文件路径方法
    def save_recent_file_path(self, file_path):
        # 写入文件路径到文本文件
        with open('recent_file.txt', 'w') as file:
            file.write(file_path)

    # 获取最近使用的文件路径方法
    def get_recent_file_path(self):
        # 如果最近使用的文件路径文件存在
        if os.path.exists('recent_file.txt'):
            # 读取文件路径
            with open('recent_file.txt', 'r') as file:
                return file.read().strip()
        return None  # 否则返回None

    # AI建议功能方法
    def ai_suggestions(self):
        # 显示功能介绍的消息框
        messagebox.showinfo("功能介绍", "功能未完成，该功能启动后将会一键代理用户微信，并为用户分析微信消息内容，筛选工作信息、生活信息和紧急信息三类。" +
                            "同时会提取用户的微信聊天训练本地AI用于模仿用户及时回复重要信息，回复时会有聊天弹窗，用户可以在这个弹窗中修改信息或直接回复。" +
                            "如果信息为紧急信息，将会暂停用户的工作模式，保存用户当前工作，并根据消息内容拨打不同的紧急打电话。" +
                            "本地AI训练目的是避免用户的个人隐私在网络传输过程中泄露，AI对于图片处理和文件处理以及音视频处理使用base64编码进行传输。")

    # 导出数据到数据库方法
    def export_to_database(self):
        # 连接数据库
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        # 创建学生表，如果不存在
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                院系 TEXT, 专业 TEXT, 班级 TEXT, 学号 TEXT, 姓名 TEXT, 年龄 INTEGER,
                出生日期 TEXT, 性别 TEXT, 科目1 REAL, 科目2 REAL, 科目3 REAL,
                科目4 REAL, 科目5 REAL, 最高分 REAL, 最低分 REAL, 平均分 REAL, 总分 REAL, 备注 TEXT
            )
        ''')
        # 清空表中的数据
        cursor.execute('DELETE FROM students')
        # 遍历学生数据，插入到数据库
        for student in self.students_data:
            cursor.execute('''
                INSERT INTO students (
                    院系, 专业, 班级, 学号, 姓名, 年龄, 出生日期, 性别, 科目1, 科目2, 科目3,
                    科目4, 科目5, 最高分, 最低分, 平均分, 总分, 备注
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [student[col] for col in self.student_tree['columns']])
        # 提交事务
        conn.commit()
        # 关闭连接
        conn.close()
        # 显示数据导出成功的消息框
        messagebox.showinfo("提示", "学生数据已导出到数据库")

    # 从数据库导入数据方法
    def import_from_database(self):
        # 连接数据库
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        # 查询所有学生数据
        cursor.execute('SELECT * FROM students')
        rows = cursor.fetchall()
        # 获取列名
        columns = [description[0] for description in cursor.description]
        # 关闭数据库连接
        conn.close()
        
        # 清空学生数据列表
        self.students_data.clear()
        # 遍历查询结果，转换为字典并添加到学生数据列表中
        for row in rows:
            student = dict(zip(columns, row))
            self.students_data.append(student)
        
        # 刷新树状视图
        self.refresh_treeview()
        # 显示数据导入成功的消息框
        messagebox.showinfo("提示", "学生数据已从数据库导入")