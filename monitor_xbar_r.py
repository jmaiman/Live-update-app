import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === BACA DATA DARI FAIL CSV ===
csv_path = r"C:\Users\mohdamal\Project Python\project_monitoring\data_checksheet.csv"
df = pd.read_csv(csv_path)

# Rename kolum untuk konsisten
df = df.rename(columns={
    'Sample1': 'P1',
    'Sample2': 'P2',
    'Sample3': 'P3',
    'Sample4': 'P4',
    'Sample5': 'P5'
})

# === KIRA X̄ DAN R ===
df['X̄'] = df[['P1', 'P2', 'P3', 'P4', 'P5']].mean(axis=1)
df['R'] = df[['P1', 'P2', 'P3', 'P4', 'P5']].max(axis=1) - df[['P1', 'P2', 'P3', 'P4', 'P5']].min(axis=1)

# === X̄-R CONTROL LIMITS ===
x_bar = df['X̄'].mean()
r_bar = df['R'].mean()
n = 5
A2 = 0.577
D3 = 0
D4 = 2.114
UCL_x = x_bar + A2 * r_bar
LCL_x = x_bar - A2 * r_bar
UCL_r = D4 * r_bar
LCL_r = D3 * r_bar

# === ALERT ZONE ===
x_alert_high = x_bar + 0.9 * (UCL_x - x_bar)
x_alert_low = x_bar - 0.9 * (x_bar - LCL_x)
r_alert_high = r_bar + 0.9 * (UCL_r - r_bar)

# === PLOT X̄-R CHART ===
fig, axs = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# X̄ Chart
axs[0].plot(df['X̄'], marker='o', color='blue', label='X̄')
axs[0].axhline(UCL_x, color='red', linestyle='--', label='UCL')
axs[0].axhline(LCL_x, color='red', linestyle='--', label='LCL')
axs[0].axhline(x_bar, color='green', linestyle='-', label='X̄-bar')
for i, val in enumerate(df['X̄']):
    if val > x_alert_high or val < x_alert_low:
        axs[0].plot(i, val, marker='^', color='gold', markersize=10)
axs[0].set_title("X̄ Chart")
axs[0].set_ylabel("Average")
axs[0].grid(True)
axs[0].legend()

# R Chart
axs[1].plot(df['R'], marker='s', color='purple', label='R')
axs[1].axhline(UCL_r, color='red', linestyle='--', label='UCL')
axs[1].axhline(LCL_r, color='red', linestyle='--', label='LCL')
axs[1].axhline(r_bar, color='green', linestyle='-', label='R-bar')
for i, val in enumerate(df['R']):
    if val > r_alert_high:
        axs[1].plot(i, val, marker='^', color='gold', markersize=10)
axs[1].set_title("R Chart")
axs[1].set_xlabel("Day")
axs[1].set_ylabel("Range")
axs[1].grid(True)
axs[1].legend()
axs[1].set_xticks(range(len(df)))
axs[1].set_xticklabels(range(1, len(df)+1))

plt.tight_layout()

# === AUTO SAVE ===
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
save_dir = r"C:\Users\mohdamal\Project Python\project_monitoring\Daily Result"
os.makedirs(save_dir, exist_ok=True)

filename = os.path.join(save_dir, f'xbar_r_chart_{timestamp}.png')
plt.savefig(filename)
print(f"[\u2714] X̄-R Chart saved as {filename}")
plt.show()

# === PLOT CPK ===
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

cpk_filename = os.path.join(save_dir, f'cpk_chart_{timestamp}.png')
plt.savefig(cpk_filename)
print(f"[\u2714] CPK Chart saved as {cpk_filename}")
plt.show()
