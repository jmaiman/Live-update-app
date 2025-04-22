import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from datetime import datetime

# =============================================
# KONFIGURASI UTAMA (SESUAIKAN JIKA PERLU)
# =============================================
FOLDER_DATA = r"Project Python\project_monitoring\Daily Result"
NAMA_FAIL = "rekod_harian.csv"
USL = 26.20
LSL = 25.90

# =============================================
# FUNGSI PEMBACAAN DATA
# =============================================
def baca_data():
    file_path = r"C:\Users\mohdamal\Project Python\project_monitoring\Daily Result\rekod_harian.csv"

    print("🔍 Path yang dicari:", os.path.abspath(file_path))

    if not os.path.exists(file_path):
        print(f"❌ Ralat: Fail '{file_path}' tidak ditemukan!")
        sys.exit(1)

    try:
        if NAMA_FAIL.endswith('.csv'):
            print(f"Path lengkap: {os.path.abspath(file_path)}")
            print(f"File exists? {os.path.exists(file_path)}")
            df = pd.read_csv(file_path, encoding='utf-8')
        elif NAMA_FAIL.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        print("✅ Data berjaya dimuatkan:")
        print(df.head(3))
        return df
    except Exception as e:
        print(f"❌ Gagal membaca fail:\n{str(e)}")
        sys.exit(1)

# =============================================
# FUNGSI UTAMA
# =============================================
def main():
    df = baca_data()

    required_cols = ['Day', 'Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']
    sample_cols = required_cols[1:]  # untuk kemudahan

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"\n❌ Kolum wajib tidak ditemui: {missing}")
        sys.exit(1)

    df.dropna(subset=required_cols, inplace=True)
    df['Day'] = pd.to_datetime(df['Day'], dayfirst=True)
    df['Day_str'] = df['Day'].dt.strftime('%d/%m')

    if len(df) < 2:
        print(f"\n⚠️ Data hanya ada {len(df)} baris. Perlu sekurang-kurangnya 2 untuk buat graf kawalan.")
        sys.exit(0)

    df['X̄'] = df[sample_cols].mean(axis=1)
    df['R'] = df[sample_cols].max(axis=1) - df[sample_cols].min(axis=1)

    Xbar_bar = df['X̄'].mean()
    R_bar = df['R'].mean()
    A2 = 0.577
    CL = Xbar_bar
    UCL = CL + A2 * R_bar
    LCL = CL - A2 * R_bar

    # Plot graf X̄
    plt.figure(figsize=(10, 5))
    plt.plot(df['Day_str'], df['X̄'], 'bo-', label='X̄')
    plt.axhline(CL, color='blue', linestyle='--', label='CL')
    plt.axhline(UCL, color='red', linestyle='--', label='UCL')
    plt.axhline(LCL, color='red', linestyle='--', label='LCL')

    plt.title(f"Graf Kawalan X̄\n{datetime.now().strftime('%d/%m/%Y %H:%M')}")
    plt.xlabel("Tarikh")
    plt.ylabel("Nilai X̄")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    os.makedirs(FOLDER_DATA, exist_ok=True)
    graf_path = os.path.join(FOLDER_DATA, f"xbar_chart_{datetime.now().strftime('%Y%m%d_%H%M')}.png")
    plt.savefig(graf_path, dpi=300, bbox_inches='tight')
    print(f"\n💾 Graf disimpan di: {os.path.abspath(graf_path)}")
    plt.show()

    # CPK Calculation
    all_samples = df[sample_cols].values.flatten()
    mean = np.mean(all_samples)
    std = np.std(all_samples, ddof=1)

    Cpu = (USL - mean) / (3*std)
    Cpl = (mean - LSL) / (3*std)
    Cpk = min(Cpu, Cpl)

    print("\n📊 LAPORAN KAWALAN KUALITI")
    print("="*40)
    print(f"Purata Proses : {mean:.4f}")
    print(f"Sisihan Piawai: {std:.4f}")
    print(f"CPK           : {Cpk:.4f}")
    print("\n📌 Status Proses:", end=" ")
    if Cpk >= 1.33:
        print("✅ MAMPU (Process Capable)")
    elif Cpk >= 1.0:
        print("⚠️ BATAS MAMPU (Marginally Capable)")
    else:
        print("❌ TIDAK MAMPU (Not Capable)")

if __name__ == "__main__":
    main()

def generate_r_chart(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Day_str'], df['R'], 'go-', label='R')
    plt.axhline(df['R'].mean(), color='green', linestyle='--', label='CL')
    plt.title("Graf Kawalan R")
    plt.xlabel("Tarikh")
    plt.ylabel("Nilai R")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # 💾 Simpan graf
    r_chart_path = os.path.join(FOLDER_DATA, f"r_chart_{datetime.now().strftime('%Y%m%d_%H%M')}.png")
    plt.savefig(r_chart_path, dpi=300, bbox_inches='tight')
    print(f"\n💾 Graf R disimpan di: {os.path.abspath(r_chart_path)}")
    plt.show()

def calculate_cpk(df):
    all_samples = df[['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5']].values.flatten()
    mean = np.mean(all_samples)
    std = np.std(all_samples, ddof=1)

    Cpu = (USL - mean) / (3 * std)
    Cpl = (mean - LSL) / (3 * std)
    Cpk = min(Cpu, Cpl)

    print("\n📊 LAPORAN KAWALAN KUALITI")
    print("="*40)
    print(f"Purata Proses : {mean:.4f}")
    print(f"Sisihan Piawai: {std:.4f}")
    print(f"CPK           : {Cpk:.4f}")
    print("\n📌 Status Proses:", end=" ")
    if Cpk >= 1.33:
        print("✅ MAMPU (Process Capable)")
    elif Cpk >= 1.0:
        print("⚠️ BATAS MAMPU (Marginally Capable)")
    else:
        print("❌ TIDAK MAMPU (Not Capable)")

    # Optional: plot histogram
    plt.figure(figsize=(8, 4))
    plt.hist(all_samples, bins=10, color='skyblue', edgecolor='black')
    plt.axvline(USL, color='red', linestyle='--', label='USL')
    plt.axvline(LSL, color='red', linestyle='--', label='LSL')
    plt.axvline(mean, color='green', linestyle='--', label='Mean')
    plt.title("Histogram CPK")
    plt.xlabel("Nilai Sample")
    plt.ylabel("Frekuensi")
    plt.legend()
    plt.tight_layout()

    cpk_chart_path = os.path.join(FOLDER_DATA, f"cpk_histogram_{datetime.now().strftime('%Y%m%d_%H%M')}.png")
    plt.savefig(cpk_chart_path, dpi=300, bbox_inches='tight')
    print(f"\n💾 Histogram CPK disimpan di: {os.path.abspath(cpk_chart_path)}")
    plt.show()
