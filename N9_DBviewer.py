import sqlite3

conn = sqlite3.connect("steam_games_info.db")
cursor = conn.cursor()

    # Create table (if not exists)
cursor.execute("""
    select * from games limit 1;
    """)

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()