import sqlite3
# Connect to SQLite database (or create it)

def insert_games_in_database(Resultat) :
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        APP_ID INT PRIMARY KEY,
        Game TEXT,
        Release_Date TEXT,
        Price TEXT,
        Genres TEXT,
        Detailed_Description TEXT,
        Header_Image TEXT,
        Supported_Languages TEXT,
        Platforms TEXT,
        Metacritic_score TEXT,
        Metacritic_url TEXT
        Steam_score INT
        Total_positive INT
        Total_negative INT
        )
    """)

    # Insert data into the database
    cursor.execute("""
    INSERT OR IGNORE INTO games (APP_ID, Game, Release_Date, Price, Genres, Detailed_Description, Header_Image, Supported_Languages, Platforms, Metacritic_score,Metacritic_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(Resultat["APP_ID"]),
        Resultat["Game"],
        Resultat.get("Release_Date", "N/A"),  # Default to "N/A"
        Resultat.get("Price", "N/A"),  # Default to "Free"
        Resultat.get("Genres", "N/A"),  # Default to "N/A"
        Resultat.get("Detailed_description", "N/A"),  # Default to "N/A"
        Resultat.get("Header_image", "N/A"),  # Default to "N/A"
        Resultat.get("Supported_languages", "N/A"),  # Default to "N/A"
        Resultat.get("Platforms", "N/A"),  # Default to "N/A"
        Resultat.get("Metacritic_score", "N/A"),  # Default to "N/A"
        Resultat.get("Metacritic_url", "N/A")  # Default to "N/A"
    ))

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute("""SELECT * FROM GAMES order by APP_ID DESC LIMIT 1""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def insert_game_review_score(APP_ID, review_score,total_positive,total_negative) :

    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    # Insert data into the database
    APP_ID=int(APP_ID)
    cursor.execute(f"""
    Update or ignore games set Steam_score = {review_score}, total_positive = {total_positive}, total_negative = {total_negative} where APP_ID = {APP_ID}
    """ )

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute(f"""SELECT game, steam_score, total_positive, total_negative, app_id FROM GAMES where APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ligne updatée : {row}")
    conn.close()


    
def insert_review_in_datalake(Resultat) :
    conn = sqlite3.connect("steam_reviews_datalake.db")
    cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
                   
        APP_ID INT PRIMARY KEY,
        Game TEXT,
        Release_Date TEXT,
        Price TEXT,
        Genres TEXT,
        Detailed_Description TEXT,
        Header_Image TEXT,
        Supported_Languages TEXT,
        Platforms TEXT,
        Metacritic_score TEXT,
        Metacritic_url TEXT
    )
    """)

    # Insert data into the database
    cursor.execute("""
    INSERT OR IGNORE INTO games (APP_ID, Game, Release_Date, Price, Genres, Detailed_Description, Header_Image, Supported_Languages, Platforms, Metacritic_score,Metacritic_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(Resultat["APP_ID"]),
        Resultat["Game"],
        Resultat.get("Release_Date", "N/A"),  # Default to "N/A"
        Resultat.get("Price", "N/A"),  # Default to "Free"
        Resultat.get("Genres", "N/A"),  # Default to "N/A"
        Resultat.get("Detailed_description", "N/A"),  # Default to "N/A"
        Resultat.get("Header_image", "N/A"),  # Default to "N/A"
        Resultat.get("Supported_languages", "N/A"),  # Default to "N/A"
        Resultat.get("Platforms", "N/A"),  # Default to "N/A"
        Resultat.get("Metacritic_score", "N/A"),  # Default to "N/A"
        Resultat.get("Metacritic_url", "N/A")  # Default to "N/A"
    ))

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute("""SELECT * FROM GAMES order by APP_ID DESC LIMIT 1""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()