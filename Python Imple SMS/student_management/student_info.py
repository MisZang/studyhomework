import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

class StudentInfoTab:
    def __init__(self, notebook, students_data, all_students_tab):
        self.frame = ttk.Frame(notebook)
        self.students_data = students_data  # 接收共享的学生数据列表
        self.all_students_tab = all_students_tab  # 引用全部学生标签页
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(expand=True, fill='both')

        labels = ["院系", "专业", "班级", "学号", "姓名", "年龄", "出生日期", "性别", "科目1", "科目2", "科目3", "科目4", "科目5", "备注"]
        self.entries = {}

        for i, text in enumerate(labels):
            label = ttk.Label(main_frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(main_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            self.entries[text] = entry
        
        self.gender = tk.StringVar()

        ttk.Radiobutton(main_frame, text='男', variable=self.gender, value='男', command=self.update_gender).grid(row=7, column=2, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(main_frame, text='女', variable=self.gender, value='女', command=self.update_gender).grid(row=7, column=3, padx=5, pady=5, sticky='w')

        # 将确认添加按钮放置在主框架的底部
        ttk.Button(self.frame, text="确认添加", command=self.add_student).pack(side='bottom', padx=5, pady=5)

    def update_gender(self):
        self.entries["性别"].delete(0, tk.END)
        self.entries["性别"].insert(0, self.gender.get())

    def add_student(self):
        student_data = {}
        for key, entry in self.entries.items():
            student_data[key] = entry.get()

        student_data["性别"] = self.gender.get()

        scores = [float(student_data[f"科目{i}"]) for i in range(1, 6) if student_data[f"科目{i}"]]

        if scores:
            student_data["最高分"] = max(scores)
            student_data["最低分"] = min(scores)
            student_data["平均分"] = sum(scores) / len(scores)
            student_data["总分"] = sum(scores)
        else:
            student_data["最高分"] = student_data["最低分"] = student_data["平均分"] = student_data["总分"] = 0

        self.students_data.append(student_data)  # 将新学生信息添加到共享数据列表
        self.all_students_tab.refresh_treeview()  # 刷新全部学生标签页的Treeview

        if self.all_students_tab.current_file_path:
            self.append_student_to_excel(self.all_students_tab.current_file_path, student_data)

        messagebox.showinfo("提示", "学生信息已添加")

    def append_student_to_excel(self, file_path, student_data):
        try:
            df = pd.read_excel(file_path)
            df = df.append(student_data, ignore_index=True)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("提示", "学生信息已添加到Excel文件")
        except Exception as e:
            messagebox.showerror("错误", f"无法将学生信息添加到Excel文件: {e}")
