# 导入Tkinter库，简化Tkinter模块的引用
import tkinter as tk
# 导入ttk模块，提供更现代的控件风格
from tkinter import ttk
# 导入messagebox模块，用于显示对话框
from tkinter import messagebox
# 导入matplotlib库中的pyplot模块，用于绘图
import matplotlib.pyplot as plt
# 导入matplotlib后端模块，用于在Tkinter窗口中嵌入图表
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# 导入pandas库，用于数据处理

# 定义一个类SearchStudentTab，用于实现查找学生的功能
class SearchStudentTab:
    # 构造函数，初始化标签页的框架和数据
    def __init__(self, notebook, students_data):
        # 创建一个ttk.Frame实例，作为标签页的内容容器
        self.frame = ttk.Frame(notebook)
        # 存储学生数据列表
        self.students_data = students_data
        # 调用create_widgets方法创建控件
        self.create_widgets()

    # 方法create_widgets，用于创建控件并布局
    def create_widgets(self):
        # 创建一个搜索框的框架
        self.search_frame = ttk.Frame(self.frame)
        # 使用grid布局管理器定位搜索框框架
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        # 创建并放置一个标签，显示“学号”
        ttk.Label(self.search_frame, text="学号").grid(row=0, column=0, padx=5, pady=5)
        # 创建并放置一个输入框，用于输入学号
        self.search_id_entry = ttk.Entry(self.search_frame)
        self.search_id_entry.grid(row=0, column=1, padx=5, pady=5)
        # 创建并放置一个按钮，用于触发查找学生功能
        ttk.Button(self.search_frame, text="查找", command=self.search_student).grid(row=0, column=2, padx=5, pady=5)

        # 创建一个画布，用于容纳滚动条和内部框架
        self.canvas = tk.Canvas(self.frame)
        # 创建一个内部框架，用于放置可滚动的内容
        self.scroll_frame = ttk.Frame(self.canvas)
        # 创建垂直滚动条，与画布关联
        self.v_scroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        # 创建水平滚动条，与画布关联
        self.h_scroll = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        # 设置画布的滚动条命令
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # 布局垂直滚动条
        self.v_scroll.grid(row=1, column=1, sticky='ns')
        # 布局水平滚动条
        self.h_scroll.grid(row=2, column=0, sticky='ew')
        # 布局画布
        self.canvas.grid(row=1, column=0, sticky='nsew')
        # 设置框架的网格权重，使其可以扩展
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # 在画布上创建一个窗口，用于显示内部框架
        self.canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        # 绑定事件，当内部框架大小改变时，调整画布的滚动区域
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # 调用方法populate_scroll_frame填充内部框架的内容
        self.populate_scroll_frame()

        # 创建一个按钮框架，用于放置按钮
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, pady=10, sticky='ew')
        # 设置按钮框架的网格权重，使其可以扩展
        button_frame.grid_columnconfigure(0, weight=1)

        # 创建并放置一个按钮，用于确认修改学生信息
        ttk.Button(button_frame, text="确认修改", command=self.modify_student).pack(side='left', padx=5, pady=5)
        # 创建并放置一个按钮，用于删除学生信息
        ttk.Button(button_frame, text="删除学生", command=self.delete_student).pack(side='left', padx=5, pady=5)

    # 方法populate_scroll_frame，用于填充内部框架的内容
    def populate_scroll_frame(self):
        # 定义显示的标签列表
        labels = ["院系", "专业", "班级", "学号", "姓名", "年龄", "出生日期", "性别", "科目1", "科目2", "科目3", "科目4", "科目5", "最高分", "最低分", "平均分", "总分", "备注"]
        # 创建字典存储标签
        self.result_labels = {}
        # 创建字典存储输入框
        self.result_entries = {}

        # 遍历标签列表，创建并放置标签和输入框
        for i, text in enumerate(labels):
            # 创建并放置标签
            label = ttk.Label(self.scroll_frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
            # 创建并放置输入框
            entry = ttk.Entry(self.scroll_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            # 将标签和输入框添加到对应的字典中
            self.result_labels[text] = label
            self.result_entries[text] = entry

        # 创建变量用于存储性别选择
        self.gender_search = tk.StringVar()
        # 创建并放置单选按钮，用于选择性别
        ttk.Radiobutton(self.scroll_frame, text='男', variable=self.gender_search, value='男').grid(row=7, column=2, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(self.scroll_frame, text='女', variable=self.gender_search, value='女').grid(row=7, column=3, padx=5, pady=5, sticky='w')

        # 创建matplotlib图表
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        # 添加一个子图
        self.ax = self.figure.add_subplot(111)
        # 创建图表组件，用于在Tkinter窗口中显示图表
        self.canvas_chart = FigureCanvasTkAgg(self.figure, self.scroll_frame)
        # 将图表组件放置在内部框架中
        self.canvas_chart.get_tk_widget().grid(row=0, column=4, rowspan=18, padx=10, pady=10)

    # 方法search_student，用于查找学生信息
    def search_student(self):
        # 获取输入的学号
        search_id = self.search_id_entry.get()
        # 遍历学生数据列表，查找匹配的学号
        for student in self.students_data:
            if student["学号"] == search_id:
                # 清空并填充输入框中的学生信息
                for key, value in student.items():
                    if key in self.result_entries:
                        self.result_entries[key].delete(0, tk.END)
                        self.result_entries[key].insert(0, value)
                # 设置性别选择框的值
                self.gender_search.set(student["性别"])

                # 提取成绩并绘制成柱状图
                scores = [float(student[f"科目{i}"]) for i in range(1, 6) if student[f"科目{i}"]]
                self.ax.clear()
                self.ax.bar(["科目1", "科目2", "科目3", "科目4", "科目5"], scores)
                # 更新图表
                self.canvas_chart.draw()

    # 方法modify_student，用于修改学生信息
    def modify_student(self):
        # 获取输入的学号
        search_id = self.search_id_entry.get()
        # 遍历学生数据列表，查找匹配的学号并更新信息
        for student in self.students_data:
            if student["学号"] == search_id:
                for key, entry in self.result_entries.items():
                    student[key] = entry.get()
                student["性别"] = self.gender_search.get()
                # 显示提示信息，告知信息已修改
                messagebox.showinfo("提示", "学生信息已修改")

    # 方法delete_student，用于删除学生信息
    def delete_student(self):
        # 获取输入的学号
        search_id = self.search_id_entry.get()
        # 遍历学生数据列表，查找并删除匹配的学号
        for i, student in enumerate(self.students_data):
            if student["学号"] == search_id:
                del self.students_data[i]
                # 显示提示信息，告知信息已删除
                messagebox.showinfo("提示", "学生信息已删除")
                # 清空输入框和图表
                self.clear_result_entries()
                break

    # 方法clear_result_entries，用于清空输入框和图表
    def clear_result_entries(self):
        # 清空所有输入框
        for entry in self.result_entries.values():
            entry.delete(0, tk.END)
        # 清空性别选择框
        self.gender_search.set('')
        # 清空图表
        self.ax.clear()
        # 更新图表
        self.canvas_chart.draw()