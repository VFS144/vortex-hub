import sqlite3

conn = sqlite3.connect('vortex_hub.db')
conn.execute("UPDATE users SET email = 'admin@example.com' WHERE username = 'admin'")
conn.commit()
conn.close()
print("Admin email updated successfully")
