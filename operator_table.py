import sqlite3

# Sambung ke fail database
conn = sqlite3.connect('rekod_harian.db')
cursor = conn.cursor()

# Cipta jadual jika belum wujud
cursor.execute('''
CREATE TABLE IF NOT EXISTS rekod_harian (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarikh TEXT NOT NULL,
    data1 REAL,
    data2 REAL,
    data3 REAL,
    data4 REAL,
    data5 REAL
)
''')

# Simpan perubahan dan tutup sambungan
conn.commit()
conn.close()

print("✅ Jadual 'rekod_harian' berjaya dicipta (atau telah wujud).")
