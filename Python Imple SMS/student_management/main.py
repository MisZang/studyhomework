import tkinter as tk
from tkinter import ttk
from student_info import StudentInfoTab
from search_student import SearchStudentTab
from all_students import AllStudentsTab
import subprocess
import sys

def check_and_install_packages():
    required_packages = ["tkinter", "pandas", "matplotlib"]
    for package in required_packages:
        try:
            if package == "tkinter":
                import tkinter
            elif package == "pandas":
                import pandas
            elif package == "matplotlib":
                import matplotlib
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def set_16_9_aspect_ratio(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the maximum size that fits 16:9 aspect ratio within the screen resolution
    target_width = screen_width
    target_height = int(screen_width / 4 * 3)

    if target_height > screen_height:
        target_height = screen_height
        target_width = int(screen_height / 3 * 4)

    # Set the window size to the calculated dimensions
    root.geometry(f"{target_width}x{target_height}")

def main():
    check_and_install_packages()

    root = tk.Tk()
    set_16_9_aspect_ratio(root)
    app = StudentManagementSystem(root)
    root.mainloop()

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("简单学生管理系统")
        self.students_data = []  # 用于存储学生信息的共享列表
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)

        self.all_students_tab = AllStudentsTab(notebook, self.students_data)
        self.student_info_tab = StudentInfoTab(notebook, self.students_data, self.all_students_tab)
        self.search_student_tab = SearchStudentTab(notebook, self.students_data)

        notebook.add(self.student_info_tab.frame, text='学生信息')
        notebook.add(self.search_student_tab.frame, text='查看学生')
        notebook.add(self.all_students_tab.frame, text='全部学生')

        notebook.pack(expand=1, fill='both')

if __name__ == "__main__":
    main()
