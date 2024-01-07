import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog

class FrequencyResponseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("频率响应可视化工具")

        # 创建标签
        ttk.Label(root, text="选择CSV文件:", font=('Helvetica', 12)).grid(row=0, column=0, pady=10)

        # 创建文件路径输入框
        self.file_entry = ttk.Entry(root, width=40)
        self.file_entry.grid(row=0, column=1, pady=10)

        # 创建浏览按钮
        self.browse_button = ttk.Button(root, text="浏览", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, pady=10)

        # 创建绘制按钮
        self.plot_button = ttk.Button(root, text="绘制频率响应图", command=self.plot_frequency_response)
        self.plot_button.grid(row=1, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV 文件', '*.csv')])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def plot_frequency_response(self):
        csv_file = self.file_entry.get()

        if csv_file:
            try:
                plot_frequency_response_from_csv(csv_file)
            except Exception as e:
                self.show_error_message(f"处理CSV文件时发生错误: {e}")
        else:
            self.show_error_message("请选择CSV文件")

    def show_error_message(self, message):
        messagebox.showerror("错误", message)

def plot_frequency_response_from_csv(csv_file):
    # 从CSV文件读取数据
    df = pd.read_csv(csv_file)

    # 获取数据
    frequencies = df['频率']
    voltages_a = df['A相电压']
    voltages_b = df['B相电压']
    voltages_c = df['C相电压']
    currents_a = df['A相电流']
    currents_b = df['B相电流']
    currents_c = df['C相电流']

    # 绘制频率响应曲线
    plt.figure(figsize=(12, 8))

    # 绘制电压幅值
    plt.subplot(2, 1, 1)
    plt.semilogx(frequencies, voltages_a, label='A相电压')
    plt.semilogx(frequencies, voltages_b, label='B相电压')
    plt.semilogx(frequencies, voltages_c, label='C相电压')
    plt.title('Voltage Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Voltage Amplitude')
    plt.grid(True)
    plt.legend()

    # 绘制电流幅值
    plt.subplot(2, 1, 2)
    plt.semilogx(frequencies, currents_a, label='A相电流')
    plt.semilogx(frequencies, currents_b, label='B相电流')
    plt.semilogx(frequencies, currents_c, label='C相电流')
    plt.title('Current Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Current Amplitude')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FrequencyResponseApp(root)
    root.mainloop()
