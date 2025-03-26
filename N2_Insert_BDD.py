import sqlite3

def insert_games_in_database(Resultat) :
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        APP_ID INT PRIMARY KEY,Game TEXT,Release_Date TEXT,Price TEXT,Is_free INT,Genres TEXT,Detailed_Description TEXT,Header_Image TEXT,
        Supported_Languages TEXT,Platforms TEXT,Metacritic_score TEXT,Metacritic_url TEXT,Steam_score INT,Total_positive INT,Total_negative INT, Last_cursor_position TXT)
        """)

    cursor.execute("""
        INSERT OR REPLACE INTO games (APP_ID, Game, Release_Date, Price, Is_free, Genres, Detailed_Description, Header_Image, Supported_Languages, Platforms, Metacritic_score,Metacritic_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            APP_ID := int(Resultat["APP_ID"]),
            Resultat["Game"],
            Resultat.get("Release_Date"), 
            Resultat.get("Price"),
            Resultat.get("Gratuit"),
            Resultat.get("Genres"),
            Resultat.get("Detailed_description"),
            Resultat.get("Header_image"),
            Resultat.get("Supported_languages"),
            Resultat.get("Platforms"),
            Resultat.get("Metacritic_score"),
            Resultat.get("Metacritic_url")))

    conn.commit()
    cursor.execute(f"""SELECT APP_ID, Game, Release_Date, Price, Genres, Platforms, Metacritic_score,Metacritic_url, Steam_score, total_positive,total_negative FROM GAMES WHERE APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Ligne updatée : {row}")
    conn.close()

def insert_game_review_score(APP_ID, query_summary) :

    review_score = query_summary["review_score"]
    total_positive = query_summary["total_positive"]
    total_negative = query_summary["total_negative"]
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    cursor.execute(f"""
    Update games set Steam_score = {review_score}, total_positive = {total_positive}, total_negative = {total_negative} where APP_ID = {APP_ID}
    """ )

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute(f"""SELECT game, Steam_score, total_positive, total_negative FROM GAMES where APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Notes updatée : {row}\n")
    conn.close()
    
def insert_review_in_database(APP_ID,Review) :
    conn = sqlite3.connect("steam_games_reviews.db")
    cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (APP_ID INT,Language TXT, Review TEXT, Is_positive INT, Upvotes INT, Funvotes INT, ID INT PRIMARY KEY)""")

    # Insert data into the database
    cursor.execute("""
        INSERT OR replace INTO reviews (APP_ID, Language, Review, Is_positive, Upvotes, Funvotes, ID)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",(
            APP_ID,
            Review.get("language"),
            Review.get("review"),
            Review.get("voted_up"),
            Review.get("votes_up"),
            Review.get("votes_funny"),
            ID := Review.get("recommendationid")))
    
    conn.commit()
    cursor.execute(f"""SELECT APP_ID, Language, ID FROM reviews where ID = {ID} """)
    rows = cursor.fetchall()
    print(rows)
    conn.close()

def insert_last_cursor_position(APP_ID,steam_cursor):
    
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    cursor.execute(f"""
        Update games set Last_cursor_position = "{steam_cursor}" where APP_ID = {APP_ID}""" )

    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute(f"""SELECT game, Last_cursor_position FROM GAMES where APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Cursor updaté : {row}\n")
    conn.close()


def insert_in_datalake():

    


    pass