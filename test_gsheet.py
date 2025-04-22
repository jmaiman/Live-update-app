import gspread
from oauth2client.service_account import ServiceAccountCredentials

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gsheets-creds.json", scope)
    client = gspread.authorize(creds)

    # Cuba buka spreadsheet
    spreadsheet = client.open("Rekod Harian Produksi")
    worksheet = spreadsheet.get_worksheet(0)  # Ambil worksheet pertama

    print("✅ Berjaya sambung ke Google Sheets.")
    print("📄 Nama Worksheet:", worksheet.title)

except Exception as e:
    print("❌ Gagal sambung ke Google Sheets:")
    print(e)
