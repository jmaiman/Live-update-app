import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
import pytz
from io import BytesIO
import gspread
from google.oauth2.service_account import Credentials
import json

# --- KONFIGURASI ---
DB_PATH = os.path.join("Daily Result", "rekod_harian.db")
EXCEL_PATH = os.path.join("Daily Result", "data_produksi.xlsx")
TABLE_NAME = "production_data"
os.makedirs("Daily Result", exist_ok=True)

# --- Fungsi Waktu Malaysia ---
def get_malaysia_time():
    return datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))

# --- Initialize Database SQLite ---
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

# --- Sambung ke Google Sheets (dengan error handling) ---
def connect_to_gsheet():
    try:
        # Guna credentials dari Streamlit Secrets
        creds_dict = json.loads(st.secrets["GSHEETS_CREDENTIALS"])
        creds = Credentials.from_service_account_info(creds_dict)
        client = gspread.authorize(creds)
        spreadsheet = client.open("Rekod Harian Produksi")
        worksheet = spreadsheet.get_worksheet(0)
        return worksheet
    except gspread.exceptions.APIError:
        st.warning("⚠️ Google Sheets API bermasalah. Sila semak sambungan atau quota.")
        return None
    except Exception as e:
        st.warning(f"⚠️ Tidak dapat sambung ke Google Sheets: {e}")
        return None

# --- Mula Aplikasi Streamlit ---
init_db()
st.title("Sistem Input Data Produksi")

with st.form("production_form"):
    col1, col2 = st.columns(2)

    with col1:
        tarikh = st.date_input("Tarikh", get_malaysia_time())
        operator = st.text_input("Nama Operator")

    with col2:
        shift = st.selectbox("Shift", ["Pagi", "Petang", "Malam"])

    st.subheader("Data Sampel")
    samples = [st.number_input(f"Sample {i+1}", min_value=25.0, max_value=27.0, step=0.01) for i in range(5)]

    if st.form_submit_button("Simpan Data"):
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

            # [2] Simpan ke Excel
            df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
            df.to_excel(EXCEL_PATH, index=False)

            # [3] Simpan ke Google Sheets
            sheet = connect_to_gsheet()
            if sheet:
                try:
                    sheet.append_row([
                        tarikh.strftime('%Y-%m-%d'),
                        operator,
                        shift,
                        *samples,
                        waktu.strftime('%Y-%m-%d %H:%M:%S')
                    ])
                except Exception as e_gs:
                    st.warning(f"⚠️ Gagal simpan ke Google Sheets: {e_gs}")
            else:
                st.info("📁 Data hanya disimpan ke Excel dan Database.")

            st.toast("✅ Data berjaya disimpan!", icon="✅")

        except Exception as e:
            st.error(f"❌ Error semasa simpan data: {str(e)}")

        finally:
            conn.close()

# --- Butang Muat Turun Excel ---
st.divider()
if os.path.exists(EXCEL_PATH):
    with open(EXCEL_PATH, "rb") as f:
        st.download_button(
            "Muat Turun Laporan Lengkap",
            f,
            file_name="data_produksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("❌ Tiada data untuk dimuat turun.")

import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
import pytz
from io import BytesIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- KONFIGURASI ---
DB_PATH = os.path.join("Daily Result", "rekod_harian.db")
EXCEL_PATH = os.path.join("Daily Result", "data_produksi.xlsx")
TABLE_NAME = "production_data"
os.makedirs("Daily Result", exist_ok=True)

# --- Fungsi Waktu Malaysia ---
def get_malaysia_time():
    return datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))

# --- Initialize Database SQLite ---
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

# --- Sambung ke Google Sheets (dengan error handling) ---
def connect_to_gsheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("gsheets-creds.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("Rekod Harian Produksi")
        worksheet = spreadsheet.get_worksheet(0)  # Ambil worksheet pertama
        return worksheet
    except gspread.exceptions.APIError:
        st.warning("⚠️ Google Sheets API bermasalah. Sila semak sambungan atau quota.")
        return None
    except Exception:
        st.warning("⚠️ Tidak dapat sambung ke Google Sheets.")
        return None

# --- Mula Aplikasi Streamlit ---
init_db()
st.title("Sistem Input Data Produksi")

with st.form("production_form"):
    col1, col2 = st.columns(2)

    with col1:
        tarikh = st.date_input("Tarikh", get_malaysia_time())
        operator = st.text_input("Nama Operator")

    with col2:
        shift = st.selectbox("Shift", ["Pagi", "Petang", "Malam"])

    st.subheader("Data Sampel")
    samples = [st.number_input(f"Sample {i+1}", min_value=25.0, max_value=27.0, step=0.01) for i in range(5)]

    if st.form_submit_button("Simpan Data"):
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

            # [2] Simpan ke Excel
            df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
            df.to_excel(EXCEL_PATH, index=False)

            # [3] Simpan ke Google Sheets
            sheet = connect_to_gsheet()
            if sheet:
                try:
                    sheet.append_row([
                        tarikh.strftime('%Y-%m-%d'),
                        operator,
                        shift,
                        *samples,
                        waktu.strftime('%Y-%m-%d %H:%M:%S')
                    ])
                except Exception as e_gs:
                    st.warning(f"⚠️ Gagal simpan ke Google Sheets: {e_gs}")
            else:
                st.info("📁 Data hanya disimpan ke Excel dan Database.")

            st.toast("✅ Data berjaya disimpan!", icon="✅")

        except Exception as e:
            st.error(f"❌ Error semasa simpan data: {str(e)}")

        finally:
            conn.close()

# --- Butang Muat Turun Excel ---
st.divider()
if os.path.exists(EXCEL_PATH):
    with open(EXCEL_PATH, "rb") as f:
        st.download_button(
            "Muat Turun Laporan Lengkap",
            f,
            file_name="data_produksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("❌ Tiada data untuk dimuat turun.")

