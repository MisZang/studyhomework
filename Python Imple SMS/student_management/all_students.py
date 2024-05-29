import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class AllStudentsTab:
    def __init__(self, notebook, students_data):
        self.frame = ttk.Frame(notebook)
        self.students_data = students_data  # 接收共享的学生数据列表
        self.current_file_path = None  # 当前打开的Excel文件路径
        self.create_widgets()
        self.load_recent_excel()  # 初始化时加载最近的Excel文件

    def create_widgets(self):
        columns = ["院系", "专业", "班级", "学号", "姓名", "年龄", "出生日期", "性别", "科目1", "科目2", "科目3", "科目4", "科目5", "最高分", "最低分", "平均分", "总分", "备注"]

        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.pack(expand=1, fill='both')

        self.student_tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100)

        # 创建滚动条
        self.v_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.h_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.student_tree.xview)

        self.student_tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.student_tree.pack(expand=1, fill='both')

        self.refresh_treeview()

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="导出为Excel", command=self.export_to_excel).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="导入Excel", command=self.import_from_excel).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="AI建议", command=self.ai_suggestions).pack(side='left', padx=5, pady=5)

    def refresh_treeview(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for student in self.students_data:
            self.student_tree.insert('', tk.END, values=[student[col] for col in self.student_tree['columns']])

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            columns = [self.student_tree.heading(col)["text"] for col in self.student_tree["columns"]]
            data = [self.student_tree.item(child)["values"] for child in self.student_tree.get_children()]
            df = pd.DataFrame(data, columns=columns)
            df.to_excel(file_path, index=False)
            self.current_file_path = file_path  # 更新当前文件路径
            self.save_recent_file_path(file_path)
            messagebox.showinfo("提示", "导出为Excel成功")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            self.load_excel(file_path)
            self.save_recent_file_path(file_path)

    def load_excel(self, file_path):
        df = pd.read_excel(file_path)
        self.students_data.clear()
        for _, row in df.iterrows():
            self.students_data.append(row.to_dict())
        self.refresh_treeview()
        self.current_file_path = file_path  # 更新当前文件路径
        messagebox.showinfo("提示", "导入Excel成功")

    def load_recent_excel(self):
        recent_file_path = self.get_recent_file_path()
        if recent_file_path and os.path.exists(recent_file_path):
            self.load_excel(recent_file_path)

    def save_recent_file_path(self, file_path):
        with open('recent_file.txt', 'w') as file:
            file.write(file_path)

    def get_recent_file_path(self):
        if os.path.exists('recent_file.txt'):
            with open('recent_file.txt', 'r') as file:
                return file.read().strip()
        return None

    def ai_suggestions(self):
        # Placeholder for AI suggestions functionality
        messagebox.showinfo("提示", "AI建议生成")
