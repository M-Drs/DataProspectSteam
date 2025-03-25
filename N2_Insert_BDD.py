import sqlite3

def insert_games_in_database(Resultat) :
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

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
        Metacritic_url TEXT,
        Steam_score INT,
        Total_positive INT,
        Total_negative INT
        )
        """)

    cursor.execute("""
    INSERT OR IGNORE INTO games (APP_ID, Game, Release_Date, Price, Genres, Detailed_Description, Header_Image, Supported_Languages, Platforms, Metacritic_score,Metacritic_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        APP_ID := int(Resultat["APP_ID"]),
        Resultat["Game"],
        Resultat.get("Release_Date"), 
        Resultat.get("Price"),  
        Resultat.get("Genres"),  
        Resultat.get("Detailed_description"),  
        Resultat.get("Header_image"),  
        Resultat.get("Supported_languages"),  
        Resultat.get("Platforms"),  
        Resultat.get("Metacritic_score"),  
        Resultat.get("Metacritic_url")  
        ))

    conn.commit()
    cursor.execute(f"""SELECT APP_ID, Game, Release_Date, Price, Genres, Platforms, Metacritic_score,Metacritic_url, Steam_score, total_positive,total_negative FROM GAMES WHERE APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def insert_game_review_score(i, query_summary) :

    APP_ID=int(i)
    review_score = query_summary["review_score"]
    total_positive = query_summary["total_positive"]
    total_negative = query_summary["total_negative"]
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    cursor.execute(f"""
    Update or ignore games set Steam_score = {review_score}, total_positive = {total_positive}, total_negative = {total_negative} where APP_ID = {APP_ID}
    """ )

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute(f"""SELECT game, Steam_score, total_positive, total_negative FROM GAMES where APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(f"score reviews updaté : {row}")
    conn.close()


    
def insert_review_in_datalake(Resultat) :
    conn = sqlite3.connect("steam_reviews_datalake.db")
    cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (     
        
                   
        )
        """)

    # Insert data into the database
    cursor.execute("""
    INSERT OR IGNORE INTO games (APP_ID, Game, Release_Date, Price, Genres, Detailed_Description, Header_Image, Supported_Languages, Platforms, Metacritic_score,Metacritic_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (


        ))

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute("""SELECT * FROM GAMES order by APP_ID DESC LIMIT 1""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()