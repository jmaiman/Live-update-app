import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# STEP 1: Setup credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(
    st.secrets["gsheets_creds"], scopes=scope)

client = gspread.authorize(creds)

# STEP 2: Open sheet (ganti ID dengan ID anda)
SHEET_ID = "1VvlcA34Odn2zLwgrIfZN2xEqqzAfQP4MO6fZIX7DU4M"
SHEET_NAME = "Sheet1"

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# STEP 3: Uji baca data
data = sheet.get_all_records()
st.write("Google Sheet URL:http\\docs.google.com/spreadsheets/d/1VvlcA34Odn2zLwgrIfZN2xEqqzAfQP4MO6fZIX7DU4M/edit#gid=0")
st.write(data) 

























