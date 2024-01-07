import os
import pandas as pd
from scipy.io import savemat
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CSVtoMATConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV转MAT工具")

        self.input_label = ttk.Label(root, text="输入CSV文件或文件夹:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.input_entry = ttk.Entry(root, width=40)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_input_button = ttk.Button(root, text="浏览", command=self.browse_input)
        self.browse_input_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        self.output_label = ttk.Label(root, text="输出MAT文件夹:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.output_entry = ttk.Entry(root, width=40)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_output_button = ttk.Button(root, text="浏览", command=self.browse_output_folder)
        self.browse_output_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        self.convert_button = ttk.Button(root, text="批量转换为MAT", command=self.convert_csv_to_mat)
        self.convert_button.grid(row=2, column=0, columnspan=3, pady=10)

    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')],
                                               title="选择单个CSV文件或选择文件夹")
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, folder_path)

    def convert_csv_to_mat(self):
        input_path = self.input_entry.get()
        output_folder = self.output_entry.get()

        if os.path.isfile(input_path):
            # 单个文件转换
            self.convert_single_csv_to_mat(input_path, output_folder)
        elif os.path.isdir(input_path):
            # 文件夹批量转换
            self.convert_folder_csv_to_mat(input_path, output_folder)
        else:
            self.show_error_message("请选择有效的CSV文件或文件夹")

    def convert_single_csv_to_mat(self, input_file, output_folder):
        try:
            # 读取CSV文件
            df = pd.read_csv(input_file)

            # 将DataFrame转换为字典
            data_dict = df.to_dict(orient='list')

            # 生成输出MAT文件路径
            output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}.mat")

            # 保存为MAT文件
            savemat(output_file, data_dict)

            self.show_success_message(f"成功转换 {input_file} 到 {output_file}")
        except Exception as e:
            self.show_error_message(f"处理 {input_file} 时发生错误: {e}")

    def convert_folder_csv_to_mat(self, input_folder, output_folder):
        for filename in os.listdir(input_folder):
            if filename.endswith(".csv"):
                input_file = os.path.join(input_folder, filename)
                self.convert_single_csv_to_mat(input_file, output_folder)

    def show_success_message(self, message):
        messagebox.showinfo("成功", message)

    def show_error_message(self, message):
        messagebox.showerror("错误", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVtoMATConverterApp(root)
    root.mainloop()
