import streamlit as st
import pandas as pd
import os
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set timezone Malaysia
tz = pytz.timezone('Asia/Kuala_Lumpur')

# Fail untuk simpan data
excel_file = "data_harian.xlsx"

# Header kolum
columns = ["Section", "Process", "Staff ID", "Tarikh", "Operator Name", "Shift",
           "Data 1", "Data 2", "Data 3", "Data 4", "Data 5", "Timestamp", "Operator Confirm"]

# Fungsi cipta fail Excel jika tiada
def create_excel_file_if_not_exists():
    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=columns)
        df.to_excel(excel_file, index=False)

# Fungsi tambah data baru
def tambah_data(data):
    df_baru = pd.DataFrame([data], columns=columns)

    # Jika fail kosong atau tiada data lama
    try:
        df_lama = pd.read_excel(excel_file)
        if not df_lama.empty:
            df_gabung = pd.concat([df_lama, df_baru], ignore_index=True)
        else:
            df_gabung = df_baru
    except Exception as e:
        # Kalau fail tiada atau gagal dibaca, terus guna data baru
        df_gabung = df_baru

    df_gabung.to_excel(excel_file, index=False)

# Fungsi kira dan paparkan graf X̄-R + CPK
def papar_graf_xbar_r_cpk():
    try:
        df = pd.read_excel(excel_file)

        # Ambil data 1 hingga 5
        data_kualiti = df[['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5']]
        xbar_list = data_kualiti.mean(axis=1)
        r_list = data_kualiti.max(axis=1) - data_kualiti.min(axis=1)

        # Tetapan spesifikasi
        LSL = 7.40
        USL = 8.30
        TARGET = 7.85

        # Hitung CPK
        overall_std = data_kualiti.stack().std()
        xbar_all = data_kualiti.stack().mean()
        cpu = (USL - xbar_all) / (3 * overall_std)
        cpl = (xbar_all - LSL) / (3 * overall_std)
        cpk = min(cpu, cpl)

        # Papar graf dalam Streamlit
        st.subheader("📊 X̄-R Chart & CPK")

        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        sns.lineplot(x=range(1, len(xbar_list)+1), y=xbar_list, ax=axs[0], marker='o')
        axs[0].axhline(TARGET, color='green', linestyle='--', label='Target')
        axs[0].axhline(USL, color='red', linestyle='--', label='USL')
        axs[0].axhline(LSL, color='red', linestyle='--', label='LSL')
        axs[0].set_title('X̄ Chart')
        axs[0].legend()

        sns.lineplot(x=range(1, len(r_list)+1), y=r_list, ax=axs[1], marker='o', color='orange')
        axs[1].set_title('R Chart')
        axs[1].set_xlabel("Sample")
        axs[1].set_ylabel("Range")

        plt.tight_layout()
        st.pyplot(fig)

        st.metric("CPK Value", f"{cpk:.3f}")

    except Exception as e:
        st.warning("Data belum mencukupi untuk jana graf atau CPK.")

# Streamlit UI
st.title("Riveting Width Process - Data Rekod")

with st.form("data_form"):
    section = st.text_input("Section")
    process = st.text_input("Process")
    staff_id = st.text_input("Staff ID")
    tarikh = st.date_input("Tarikh")
    operator_name = st.text_input("Operator Name")
    shift = st.selectbox("Shift", ["Pagi", "Petang", "Malam"])
    data1 = st.number_input("Data 1 (mm)", min_value=0.0, format="%.2f")
    data2 = st.number_input("Data 2 (mm)", min_value=0.0, format="%.2f")
    data3 = st.number_input("Data 3 (mm)", min_value=0.0, format="%.2f")
    data4 = st.number_input("Data 4 (mm)", min_value=0.0, format="%.2f")
    data5 = st.number_input("Data 5 (mm)", min_value=0.0, format="%.2f")
    operator_confirm = st.checkbox("Saya sahkan data ini betul")

    submitted = st.form_submit_button("Hantar Data")

    if submitted:
        if not all([section, process, staff_id, operator_name]) or not operator_confirm:
            st.error("Sila lengkapkan semua maklumat dan sahkan sebelum hantar.")
        else:
            timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            data = [section, process, staff_id, str(tarikh), operator_name, shift,
                    data1, data2, data3, data4, data5, timestamp, operator_confirm]
            create_excel_file_if_not_exists()
            tambah_data(data)
            st.success("Data berjaya direkod.")
            papar_graf_xbar_r_cpk()