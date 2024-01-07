import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging  # 添加 logging 模块导入
from ttkthemes import ThemedStyle


class CodeExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("代码执行器")

        # 设置主题样式
        self.style = ThemedStyle(root)
        self.style.set_theme("plastik")

        # 设置主窗口大小
        self.root.geometry("500x380")

        # 创建标签
        ttk.Label(root, text="选择要执行的工具:", font=('Helvetica', 14)).grid(row=0, column=0, columnspan=3, pady=10)

        # 创建自定义样式
        self.custom_style = ttk.Style()
        self.custom_style.configure("Custom.TButton", font=('Helvetica', 12))

        # 将按钮居中放置在第2行的第1列
        self.code1_button = ttk.Button(root, text="CSV剪切工具", command=self.run_code1, style="Custom.TButton")
        self.code1_button.grid(row=1, column=800, pady=20, sticky=tk.W + tk.E)

        self.code2_button = ttk.Button(root, text="合并CSV文件工具", command=self.run_code2, style="Custom.TButton")
        self.code2_button.grid(row=2, column=800, pady=20, sticky=tk.W + tk.E)

        self.code3_button = ttk.Button(root, text="CSV转MAT工具", command=self.run_code3, style="Custom.TButton")
        self.code3_button.grid(row=3, column=800, pady=20, sticky=tk.W + tk.E)

        # 设置日志记录
        logging.basicConfig(filename='code_executor.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s')

    def run_code1(self):
        script_path = "剪切.py"  # 请根据实际路径调整
        self.run_script(script_path, "CSV剪切工具")

    def run_code2(self):
        script_path = "合并.py"  # 请根据实际路径调整
        self.run_script(script_path, "合并CSV文件工具")

    def run_code3(self):
        script_path = "csv转化为mat格式.py"  # 请根据实际路径调整
        self.run_script(script_path, "CSV转MAT工具")

    def run_script(self, script_path, tool_name):
        if os.path.exists(script_path):
            try:
                subprocess.run(["python", script_path])
                self.show_success_message(f"{tool_name} 脚本运行成功")
                logging.info(f"{tool_name} 脚本运行成功")
            except Exception as e:
                error_message = f"{tool_name} 脚本运行时发生错误: {e}"
                self.show_error_message(error_message)
                logging.error(error_message)
        else:
            error_message = f"{script_path} 文件不存在"
            self.show_error_message(error_message)
            logging.error(error_message)

    def show_success_message(self, message):
        messagebox.showinfo("成功", message)

    def show_error_message(self, message):
        messagebox.showerror("错误", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeExecutorApp(root)
    root.mainloop()
