import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
import pytz
from io import BytesIO

# Konfigurasi
DB_PATH = os.path.join("Daily Result", "rekod_harian.db")
EXCEL_PATH = os.path.join("Daily Result", "data_produksi.xlsx")  # NAMA FILE TETAP
TABLE_NAME = "production_data"
os.makedirs("Daily Result", exist_ok=True)  # Buat folder jika belum ada

# Fungsi Waktu Malaysia
def get_malaysia_time():
    return datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarikh DATE NOT NULL,
        operator_name TEXT,
        shift TEXT,
        sample1 REAL NOT NULL,
        sample2 REAL NOT NULL,
        sample3 REAL NOT NULL,
        sample4 REAL NOT NULL,
        sample5 REAL NOT NULL,
        timestamp DATETIME
    )
    """)
    conn.commit()
    conn.close()

init_db()

# UI Aplikasi
st.title("📋 Sistem Input Data Produksi")

with st.form("production_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        tarikh = st.date_input("Tarikh", get_malaysia_time())
        operator = st.text_input("Nama Operator")
    
    with col2:
        shift = st.selectbox("Shift", ["Pagi", "Petang", "Malam"])
    
    st.subheader("Data Sampel")
    samples = [st.number_input(f"Sample {i+1}", min_value=25.0, max_value=27.0, step=0.01) for i in range(5)]
    
    if st.form_submit_button("💾 Simpan Data"):
        try:
            waktu = get_malaysia_time()
            
            # [1] Simpan ke SQLite
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                f"""INSERT INTO {TABLE_NAME} VALUES (
                    NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )""", 
                (
                    tarikh.strftime('%Y-%m-%d'),
                    operator,
                    shift,
                    *samples,
                    waktu.strftime('%Y-%m-%d %H:%M:%S')
                )
            )
            conn.commit()
            
            # [2] Update Excel (OVERWRITE FILE YANG SAMA)
            df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
            df.to_excel(EXCEL_PATH, index=False)  # File sama akan ditimpa
            
            st.toast("✅ Data disimpan!", icon="✅")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        finally:
            conn.close()

# Download Button (File Excel Terkini)
st.divider()
if os.path.exists(EXCEL_PATH):
    with open(EXCEL_PATH, "rb") as f:
        st.download_button(
            "⬇️ Muat Turun Laporan Lengkap",
            f,
            file_name="data_produksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("Tiada data lagi")