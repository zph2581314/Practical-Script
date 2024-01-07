import os
import pandas as pd
import chardet
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CSVCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV剪切工具")

        self.input_label = ttk.Label(root, text="输入文件夹:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.input_entry = ttk.Entry(root, width=40)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_input_button = ttk.Button(root, text="浏览", command=self.browse_input_folder)
        self.browse_input_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        self.output_label = ttk.Label(root, text="输出文件夹:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.output_entry = ttk.Entry(root, width=40)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_output_button = ttk.Button(root, text="浏览", command=self.browse_output_folder)
        self.browse_output_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        self.start_row_label = ttk.Label(root, text="起始行:")
        self.start_row_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.start_row_entry = ttk.Entry(root)
        self.start_row_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.end_row_label = ttk.Label(root, text="结束行:")
        self.end_row_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.end_row_entry = ttk.Entry(root)
        self.end_row_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self.cut_button = ttk.Button(root, text="剪切CSV", command=self.cut_csv)
        self.cut_button.grid(row=4, column=0, columnspan=3, pady=10)

    def browse_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, folder_path)

    def detect_file_encoding(self, file_path):
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding']

    def cut_csv(self):
        input_folder = self.input_entry.get()
        output_folder = self.output_entry.get()
        start_row = int(self.start_row_entry.get())
        end_row = int(self.end_row_entry.get())

        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):
            if filename.endswith(".csv"):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, f"cut_{filename}")

                try:
                    file_encoding = self.detect_file_encoding(input_path)
                    df = pd.read_csv(input_path, encoding=file_encoding)
                    df_cut = df.iloc[start_row - 1:end_row]
                    df_cut.to_csv(output_path, encoding=file_encoding, index=False)
                    print(f"成功剪切 {input_path} 至 {output_path}")
                    self.show_success_message(f"成功剪切 {input_path} 至 {output_path}")
                except PermissionError as pe:
                    print(f"{input_path} 权限错误: {pe}")
                except Exception as e:
                    print(f"{input_path} 处理错误: {e}")

    def show_success_message(self, message):
        messagebox.showinfo("成功", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVCutterApp(root)
    root.mainloop()
