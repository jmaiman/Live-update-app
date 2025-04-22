import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

# Folder simpan data
save_dir = r'C:\Users\mohdamal\Project Python\project_monitoring\Daily Result'
os.makedirs(save_dir, exist_ok=True)

# Parameter kawalan
USL = 26.20
LSL = 25.90

# Fungsi jana graf Xbar, R, dan CPK
def generate_graph():
    file_path = os.path.join(save_dir, 'rekod_harian.csv')
    if not os.path.exists(file_path):
        return

    try:
        df = pd.read_csv(file_path)
        required_cols = ['Day', 'Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']
        if not all(col in df.columns for col in required_cols):
            return

        df.dropna(subset=required_cols, inplace=True)
        df['Day'] = pd.to_datetime(df['Day'], dayfirst=True)
        df['Day_str'] = df['Day'].dt.strftime('%d/%m')

        if len(df) < 2:
            return

        df['X̄'] = df[['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']].mean(axis=1)
        df['R'] = df[['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']].max(axis=1) - df[['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']].min(axis=1)

        Xbar_bar = df['X̄'].mean()
        R_bar = df['R'].mean()
        A2 = 0.577
        CL = Xbar_bar
        UCL = CL + A2 * R_bar
        LCL = CL - A2 * R_bar

        # Plot X̄ chart
        plt.figure(figsize=(10, 5))
        plt.plot(df['Day_str'], df['X̄'], 'bo-', label='X̄')
        plt.axhline(CL, color='blue', linestyle='--', label='CL')
        plt.axhline(UCL, color='red', linestyle='--', label='UCL')
        plt.axhline(LCL, color='red', linestyle='--', label='LCL')
        plt.title(f"Graf Kawalan X̄ - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        plt.xlabel("Tarikh")
        plt.ylabel("Nilai X̄")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f"xbar_chart_{datetime.now().strftime('%Y%m%d_%H%M')}.png"), dpi=300)
        plt.close()

        # Kira CPK
        all_samples = df[['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']].values.flatten()
        mean = np.mean(all_samples)
        std = np.std(all_samples, ddof=1)
        Cpu = (USL - mean) / (3*std)
        Cpl = (mean - LSL) / (3*std)
        Cpk = min(Cpu, Cpl)

        print("\n📊 LAPORAN CPK")
        print("="*40)
        print(f"Purata Proses : {mean:.4f}")
        print(f"Sisihan Piawai: {std:.4f}")
        print(f"CPK           : {Cpk:.4f}")

    except Exception as e:
        print(f"Ralat semasa jana graf: {e}")


def save_data():
    try:
        samples = [float(e.get()) for e in entries]
        today = datetime.now().strftime('%d/%m/%Y')

        new_row = pd.DataFrame([[today] + samples], columns=['Day', 'Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5'])
        file_path = os.path.join(save_dir, 'rekod_harian.csv')

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row

        df.to_csv(file_path, index=False)
        messagebox.showinfo("Berjaya", f"Data untuk {today} disimpan.")

        # Kosongkan entri
        for e in entries:
            e.delete(0, tk.END)

        # Jana graf selepas simpan
        generate_graph()

    except ValueError:
        messagebox.showerror("Ralat", "Sila masukkan nombor sah untuk semua sample.")


# GUI setup
root = tk.Tk()
root.title("Daily Checklist - Operator")

tk.Label(root, text="Masukkan 5 bacaan hari ini:").grid(row=0, columnspan=2, pady=10)

entries = []
for i in range(5):
    tk.Label(root, text=f"Sample {i+1}").grid(row=i+1, column=0, sticky='e')
    entry = tk.Entry(root)
    entry.grid(row=i+1, column=1)
    entries.append(entry)

tk.Button(root, text="Simpan Data", command=save_data).grid(row=6, columnspan=2, pady=20)

root.mainloop()
