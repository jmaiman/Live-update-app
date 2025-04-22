import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def pilih_fail():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
    if filepath:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, filepath)

def proses_chart():
    path = entry_path.get()
    if not os.path.exists(path):
        messagebox.showerror("Ralat", "Fail tidak dijumpai!")
        return

    try:
        # Baca data
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        # Hanya ambil kolum nombor
        df = df.select_dtypes(include='number')

        # Pastikan cukup 5 kolum
        if df.shape[1] < 5:
            messagebox.showerror("Ralat", "Fail perlu ada sekurang-kurangnya 5 kolum data.")
            return

        # Ambil hanya 5 kolum pertama
        df = df.iloc[:, :5]
        df['X̄'] = df.mean(axis=1)
        df['R'] = df.max(axis=1) - df.min(axis=1)

        x_bar = df['X̄'].mean()
        r_bar = df['R'].mean()
        A2 = 0.577
        D3 = 0
        D4 = 2.114
        UCL_x = x_bar + A2 * r_bar
        LCL_x = x_bar - A2 * r_bar
        UCL_r = D4 * r_bar
        LCL_r = D3 * r_bar

        x_alert_high = x_bar + 0.9 * (UCL_x - x_bar)
        x_alert_low = x_bar - 0.9 * (x_bar - LCL_x)
        r_alert_high = r_bar + 0.9 * (UCL_r - r_bar)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Plot X̄-R Chart
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        axs[0].plot(df['X̄'], marker='o', color='blue', label='X̄')
        axs[0].axhline(UCL_x, color='red', linestyle='--', label='UCL')
        axs[0].axhline(LCL_x, color='red', linestyle='--', label='LCL')
        axs[0].axhline(x_bar, color='green', linestyle='-', label='X̄-bar')
        for i, val in enumerate(df['X̄']):
            if val > x_alert_high or val < x_alert_low:
                axs[0].plot(i, val, marker='^', color='gold', markersize=10)
        axs[0].set_title("X̄ Chart")
        axs[0].set_ylabel("Average")
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(df['R'], marker='s', color='purple', label='R')
        axs[1].axhline(UCL_r, color='red', linestyle='--', label='UCL')
        axs[1].axhline(LCL_r, color='red', linestyle='--', label='LCL')
        axs[1].axhline(r_bar, color='green', linestyle='-', label='R-bar')
        for i, val in enumerate(df['R']):
            if val > r_alert_high:
                axs[1].plot(i, val, marker='^', color='gold', markersize=10)
        axs[1].set_title("R Chart")
        axs[1].set_ylabel("Range")
        axs[1].set_xlabel("Day")
        axs[1].legend()
        axs[1].grid(True)
        axs[1].set_xticks(range(len(df)))
        axs[1].set_xticklabels(range(1, len(df)+1))

        plt.tight_layout()
        xbar_filename = f'xbar_r_chart_{timestamp}.png'
        plt.savefig(xbar_filename)
        plt.show()

        # CPK chart
        USL = 26.2
        LSL = 25.9
        mu = df['X̄'].mean()
        sigma = df['X̄'].std(ddof=1)
        cpk = min((USL - mu) / (3 * sigma), (mu - LSL) / (3 * sigma))

        plt.figure(figsize=(10, 5))
        plt.hist(df['X̄'], bins=10, color='skyblue', edgecolor='black', density=True)
        plt.axvline(mu, color='green', linestyle='--', label=f'Mean = {mu:.3f}')
        plt.axvline(USL, color='red', linestyle='--', label='USL')
        plt.axvline(LSL, color='red', linestyle='--', label='LSL')
        plt.title(f'CPK Chart\nCPK = {cpk:.3f}')
        plt.xlabel('Measurement')
        plt.ylabel('Density')
        plt.grid(True)
        plt.legend()
        cpk_filename = f'cpk_chart_{timestamp}.png'
        plt.savefig(cpk_filename)
        plt.show()

        messagebox.showinfo("Berjaya", f"Graf disimpan sebagai:\n{xbar_filename}\n{cpk_filename}")

    except Exception as e:
        messagebox.showerror("Ralat", str(e))

# ==== GUI ====
root = tk.Tk()
root.title("Mini SPC Chart Generator")

tk.Label(root, text="Pilih Fail Data:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_path = tk.Entry(root, width=50)
entry_path.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=pilih_fail).grid(row=0, column=2, padx=5, pady=5)
tk.Button(root, text="Proses & Jana Chart", bg="green", fg="white", command=proses_chart).grid(row=1, column=1, pady=10)

root.mainloop()
