import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class SearchStudentTab:
    def __init__(self, notebook, students_data):
        self.frame = ttk.Frame(notebook)
        self.students_data = students_data  # 接收共享的学生数据列表
        self.create_widgets()

    def create_widgets(self):
        self.search_frame = ttk.Frame(self.frame)
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        ttk.Label(self.search_frame, text="学号").grid(row=0, column=0, padx=5, pady=5)
        self.search_id_entry = ttk.Entry(self.search_frame)
        self.search_id_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.search_frame, text="查找", command=self.search_student).grid(row=0, column=2, padx=5, pady=5)

        self.search_result_frame = ttk.Frame(self.frame)
        self.search_result_frame.grid(row=1, column=0, padx=10, pady=10, sticky='n')

        labels = ["院系", "专业", "班级", "学号", "姓名", "年龄", "出生日期", "科目1", "科目2", "科目3", "科目4", "科目5", "最高分", "最低分", "平均分", "总分", "备注"]
        self.result_labels = {}
        self.result_entries = {}

        for i, text in enumerate(labels):
            label = ttk.Label(self.search_result_frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.search_result_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            self.result_labels[text] = label
            self.result_entries[text] = entry
        
        self.gender_search = tk.StringVar()

        ttk.Radiobutton(self.search_result_frame, text='男', variable=self.gender_search, value='男').grid(row=7, column=2, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(self.search_result_frame, text='女', variable=self.gender_search, value='女').grid(row=7, column=3, padx=5, pady=5, sticky='w')

        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.search_result_frame)
        self.canvas.get_tk_widget().grid(row=0, column=4, rowspan=18, padx=10, pady=10)

        button_frame = ttk.Frame(self.search_result_frame)
        button_frame.grid(row=18, column=0, columnspan=4, pady=10)
        ttk.Button(button_frame, text="确认修改", command=self.modify_student).pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="删除学生", command=self.delete_student).pack(side='left', padx=5, pady=5)

    def search_student(self):
        search_id = self.search_id_entry.get()
        for student in self.students_data:
            if student["学号"] == search_id:
                for key, value in student.items():
                    if key in self.result_entries:
                        self.result_entries[key].delete(0, tk.END)
                        self.result_entries[key].insert(0, value)
                self.gender_search.set(student["性别"])

                scores = [float(student[f"科目{i}"]) for i in range(1, 6) if student[f"科目{i}"]]
                self.ax.clear()
                self.ax.bar(["科目1", "科目2", "科目3", "科目4", "科目5"], scores)
                self.canvas.draw()
                break
        else:
            messagebox.showinfo("提示", "未找到该学号的学生信息")

    def modify_student(self):
        search_id = self.search_id_entry.get()
        for student in self.students_data:
            if student["学号"] == search_id:
                for key, entry in self.result_entries.items():
                    student[key] = entry.get()

                if self.all_students_tab.current_file_path:
                    self.update_student_in_excel(self.all_students_tab.current_file_path, student)

                self.all_students_tab.refresh_treeview()  # 刷新全部学生标签页的Treeview
                messagebox.showinfo("提示", "学生信息已修改")
                break

    def delete_student(self):
        search_id = self.search_id_entry.get()
        for i, student in enumerate(self.students_data):
            if student["学号"] == search_id:
                del self.students_data[i]

                if self.all_students_tab.current_file_path:
                    self.delete_student_from_excel(self.all_students_tab.current_file_path, search_id)

                self.all_students_tab.refresh_treeview()  # 刷新全部学生标签页的Treeview
                messagebox.showinfo("提示", "学生信息已删除")
                break

    def update_student_in_excel(self, file_path, updated_student):
        try:
            df = pd.read_excel(file_path)
            for i, row in df.iterrows():
                if row["学号"] == updated_student["学号"]:
                    df.iloc[i] = updated_student
                    break
            df.to_excel(file_path, index=False)
            messagebox.showinfo("提示", "学生信息已更新到Excel文件")
        except Exception as e:
            messagebox.showerror("错误", f"无法将学生信息更新到Excel文件: {e}")

    def delete_student_from_excel(self, file_path, student_id):
        try:
            df = pd.read_excel(file_path)
            df = df[df["学号"] != student_id]
            df.to_excel(file_path, index=False)
            messagebox.showinfo("提示", "学生信息已从Excel文件中删除")
        except Exception as e:
            messagebox.showerror("错误", f"无法从Excel文件中删除学生信息: {e}")
