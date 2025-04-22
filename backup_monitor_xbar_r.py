import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# === BACA DATA DARI FAIL (ganti ini dengan path fail Excel/CSV anda) ===
# df = pd.read_excel('data.xlsx')  # jika dari Excel
# Untuk demo: generate 31 hari data rawak sekitar 26.0 - 26.2
np.random.seed(42)
data = np.random.normal(loc=26.08, scale=0.05, size=(31, 5))  # 31 hari x 5 sample
df = pd.DataFrame(data, columns=['P1', 'P2', 'P3', 'P4', 'P5'])

# === KIRA X̄ DAN R ===
df['X̄'] = df.mean(axis=1)
df['R'] = df.max(axis=1) - df.min(axis=1)

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

# Set X axis ticks 1-31
axs[1].set_xticks(range(31))
axs[1].set_xticklabels(range(1, 32))

plt.tight_layout()

# === AUTO SAVE ===
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'xbar_r_chart_{timestamp}.png'
plt.savefig (filename)
print(f"[✔] X̄-R Chart saved as {filename}")
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

# Auto save CPK chart
cpk_filename = f'cpk_chart_{timestamp}.png'
plt.savefig(cpk_filename)
print(f"[✔] CPK Chart saved as {cpk_filename}")
plt.show()
