import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Mat数据截取可视化工具:
    def __init__(self, root):
        self.root = root
        self.root.title("MAT数据截取可视化工具")

        self.file_label = ttk.Label(root, text="选择MAT文件:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.file_entry = ttk.Entry(root, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_file_button = ttk.Button(root, text="浏览", command=self.browse_mat_file)
        self.browse_file_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        self.start_label = ttk.Label(root, text="起始索引:")
        self.start_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.start_entry = ttk.Entry(root)
        self.start_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.end_label = ttk.Label(root, text="结束索引:")
        self.end_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.end_entry = ttk.Entry(root)
        self.end_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.block_size_label = ttk.Label(root, text="数据块大小:")
        self.block_size_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.block_size_entry = ttk.Entry(root)
        self.block_size_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self.step_label = ttk.Label(root, text="步长:")
        self.step_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        self.step_entry = ttk.Entry(root)
        self.step_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self.save_label = ttk.Label(root, text="保存文件名:")
        self.save_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        self.save_entry = ttk.Entry(root)
        self.save_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        self.save_button = ttk.Button(root, text="选择保存位置", command=self.browse_save_location)
        self.save_button.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)

        self.extract_button = ttk.Button(root, text="截取、可视化和保存", command=self.extract_visualize_and_save)
        self.extract_button.grid(row=6, column=0, columnspan=3, pady=10)

    def browse_mat_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MAT 文件", "*.mat")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def browse_save_location(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".mat", filetypes=[('MAT 文件', '*.mat')])
        self.save_entry.delete(0, tk.END)
        self.save_entry.insert(0, save_path)

    def extract_visualize_and_save(self):
        mat_file_path = self.file_entry.get()
        start_index = int(self.start_entry.get())
        end_index = int(self.end_entry.get())
        block_size = int(self.block_size_entry.get())
        step = int(self.step_entry.get())

        try:
            # 从MAT文件中读取数据
            mat_data = scipy.io.loadmat(mat_file_path)

            # 假设MAT文件中的数据存储在变量 'data_var' 中
            data_var = 'data_var'
            data = mat_data[data_var]

            # 提取、可视化和保存数据块
            extracted_data = self.extract_and_visualize(data, start_index, end_index, block_size, step)

            # 保存处理后的数据为新的MAT文件
            save_path = self.save_entry.get()
            if save_path:
                new_mat_data = {'processed_data': extracted_data}
                scipy.io.savemat(save_path, new_mat_data)
                self.show_success_message(f"成功保存处理后的数据到 {save_path}")

        except Exception as e:
            self.show_error_message(f"处理MAT文件时发生错误: {e}")

    def extract_and_visualize(self, data, start_index, end_index, block_size, step):
        extracted_data = np.empty((data.shape[0], 0))

        for i in range(start_index-1, end_index, step):
            if i + block_size <= end_index:
                block = data[:, i:i+block_size]
                extracted_data = np.concatenate((extracted_data, block), axis=1)

                # 可视化操作，这里假设数据是一维的
                plt.plot(np.squeeze(block))
                plt.title(f'提取的数据块 {i+1} - {i+block_size}')
                plt.xlabel('样本索引')
                plt.ylabel('数值')
                plt.show()

        return extracted_data

    def show_success_message(self, message):
        messagebox.showinfo("成功", message)

    def show_error_message(self, message):
        messagebox.showerror("错误", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = Mat数据截取可视化工具(root)
    root.mainloop()
