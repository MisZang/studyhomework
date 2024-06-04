# 导入tkinter库简化引用
import tkinter as tk
# 导入ttk模块，提供高级小部件
from tkinter import ttk
# 导入messagebox模块，用于弹出消息对话框
from tkinter import messagebox
# 导入pandas库，用于数据处理和分析
from turtle import pd

# 定义学生信息标签页的类
class StudentInfoTab:
    # 初始化方法，创建标签页框架和绑定数据
    def __init__(self, notebook, students_data, all_students_tab):
        # 创建ttk.Frame实例作为标签页的主框架
        self.frame = ttk.Frame(notebook)
        # 保存学生数据列表
        self.students_data = students_data
        # 保存所有学生标签页的引用
        self.all_students_tab = all_students_tab
        # 调用create_widgets方法创建界面元素
        self.create_widgets()

    # 创建界面元素的方法
    def create_widgets(self):
        # 创建主框架，使用pack布局管理器
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(expand=True, fill='both')  # 扩展并填充整个空间
        
        # 定义需要显示的标签名列表
        labels = ["院系", "专业", "班级", "学号", "姓名", "年龄", "出生日期", "性别", "科目1", "科目2", "科目3", "科目4", "科目5", "备注"]
        # 创建一个字典来存储输入框对象
        self.entries = {}

        # 循环创建标签和输入框
        for i, text in enumerate(labels):
            # 创建标签，并设置位置
            label = ttk.Label(main_frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')  # 右对齐
            # 创建输入框，并设置位置
            entry = ttk.Entry(main_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')  # 左对齐
            # 将输入框添加到字典中
            self.entries[text] = entry

        # 创建性别变量
        self.gender = tk.StringVar()
        # 创建男性单选按钮，关联性别变量和更新性别方法
        ttk.Radiobutton(main_frame, text='男', variable=self.gender, value='男', command=self.update_gender).grid(row=7, column=2, padx=5, pady=5, sticky='w')
        # 创建女性单选按钮，关联性别变量和更新性别方法
        ttk.Radiobutton(main_frame, text='女', variable=self.gender, value='女', command=self.update_gender).grid(row=7, column=3, padx=5, pady=5, sticky='w')

        # 创建确认添加按钮，关联add_student方法
        ttk.Button(self.frame, text="确认添加", command=self.add_student).pack(side='bottom', padx=5, pady=5)

    # 更新性别输入框的方法
    def update_gender(self):
        # 清空性别输入框
        self.entries["性别"].delete(0, tk.END)
        # 插入性别变量的值到性别输入框
        self.entries["性别"].insert(0, self.gender.get())

    # 添加学生信息的方法
    def add_student(self):
        # 创建字典存储学生数据
        student_data = {}
        # 从输入框收集数据
        for key, entry in self.entries.items():
            student_data[key] = entry.get()

        # 设置性别
        student_data["性别"] = self.gender.get()
        # 收集科目分数并计算统计值
        scores = [float(student_data[f"科目{i}"]) for i in range(1, 6) if student_data[f"科目{i}"]]
        if scores:
            student_data["最高分"] = max(scores)
            student_data["最低分"] = min(scores)
            student_data["平均分"] = sum(scores) / len(scores)
            student_data["总分"] = sum(scores)
        else:
            # 如果没有成绩，设成绩相关字段为0
            student_data["最高分"] = student_data["最低分"] = student_data["平均分"] = student_data["总分"] = 0

        # 将学生数据添加到学生数据列表
        self.students_data.append(student_data)
        # 刷新所有学生标签页的树状视图
        self.all_students_tab.refresh_treeview()

        # 如果有当前文件路径，尝试将学生数据添加到Excel文件
        if self.all_students_tab.current_file_path:
            self.append_student_to_excel(self.all_students_tab.current_file_path, student_data)

        # 显示添加成功消息
        messagebox.showinfo("提示", "学生信息已添加")

    # 向Excel文件追加学生信息的方法
    def append_student_to_excel(self, file_path, student_data):
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            # 将学生数据追加到DataFrame，忽略索引
            df = df.append(student_data, ignore_index=True)
            # 写回Excel文件，不包含索引
            df.to_excel(file_path, index=False)
            # 显示添加到Excel文件成功的消息
            messagebox.showinfo("提示", "学生信息已添加到Excel文件")
        except Exception as e:
            # 捕获异常，显示错误消息
            messagebox.showerror("错误", f"无法将学生信息添加到Excel文件: {e}")