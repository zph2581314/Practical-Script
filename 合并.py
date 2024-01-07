import os
import pandas as pd
from xpinyin import Pinyin
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class 合并CSV文件工具:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV文件批量合并工具")

        self.input_label = ttk.Label(root, text="输入CSV文件夹:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.input_entry = ttk.Entry(root, width=40)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_input_button = ttk.Button(root, text="浏览", command=self.browse_input_folder)
        self.browse_input_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        self.output_label = ttk.Label(root, text="输出合并后CSV文件:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.output_entry = ttk.Entry(root, width=40)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_output_button = ttk.Button(root, text="浏览", command=self.browse_output_file)
        self.browse_output_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        self.order_label = ttk.Label(root, text="选择合并顺序:")
        self.order_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.order_var = tk.StringVar()
        self.order_var.set("按拼音首字母")  # 默认按拼音首字母顺序合并

        self.order_combobox = ttk.Combobox(root, values=["按拼音首字母", "按拼音全拼", "按文件名长度", "按文件大小", "按文件创建时间", "按数字大小"], textvariable=self.order_var)
        self.order_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

        self.merge_button = ttk.Button(root, text="批量合并CSV", command=self.merge_csv_files)
        self.merge_button.grid(row=3, column=0, columnspan=3, pady=10)

    def browse_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, folder_path)

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[('CSV 文件', '*.csv')])
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, file_path)

    def pinyin_sort(self, filenames):
        pinyin = Pinyin()
        return sorted(filenames, key=lambda x: pinyin.get_pinyin(x, ''))

    def extract_number(self, s):
        # 从字符串中提取数字部分
        match = re.search(r'\d+', s)
        return int(match.group()) if match else 0

    def merge_csv_files(self):
        input_folder = self.input_entry.get()
        output_file = self.output_entry.get()
        merge_order = self.order_var.get()

        try:
            combined_data = pd.DataFrame()

            if merge_order == "按拼音首字母":
                files_to_merge = self.pinyin_sort([f for f in os.listdir(input_folder) if f.endswith(".csv")])
            elif merge_order == "按拼音全拼":
                files_to_merge = self.pinyin_sort([f for f in os.listdir(input_folder) if f.endswith(".csv")])
            elif merge_order == "按文件名长度":
                files_to_merge = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")], key=len)
            elif merge_order == "按文件大小":
                files_to_merge = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")],
                                        key=lambda f: os.path.getsize(os.path.join(input_folder, f)))
            elif merge_order == "按文件创建时间":
                files_to_merge = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")],
                                        key=lambda f: os.path.getctime(os.path.join(input_folder, f)))
            elif merge_order == "按数字大小":
                files_to_merge = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")],
                                        key=lambda f: self.extract_number(f))

            for filename in files_to_merge:
                file_path = os.path.join(input_folder, filename)
                df = pd.read_csv(file_path)
                combined_data = pd.concat([combined_data, df], ignore_index=True)

            combined_data.to_csv(output_file, index=False)
            self.show_success_message(f"成功合并CSV文件到 {output_file}")
        except Exception as e:
            self.show_error_message(f"处理CSV文件时发生错误: {e}")

    def show_success_message(self, message):
        messagebox.showinfo("成功", message)

    def show_error_message(self, message):
        messagebox.showerror("错误", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = 合并CSV文件工具(root)
    root.mainloop()
