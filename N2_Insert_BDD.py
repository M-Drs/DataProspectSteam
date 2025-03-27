import os, time, sqlite3, json

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
    
    # Commit the transaction and close the connection
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
    Update games set Steam_score = {review_score}, total_positive = {total_positive}, total_negative = {total_negative} where APP_ID = {APP_ID}""" )
    
    # Commit the transaction and close the connection
    conn.commit()
    cursor.execute(f"""SELECT game, Steam_score, total_positive, total_negative FROM GAMES where APP_ID = {APP_ID}""")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Notes updatée : {row}\n")
    conn.close()
    
def insert_review_in_database(APP_ID,Review) :
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (APP_ID INT,Language TXT, Review TEXT, Is_positive INT, Upvotes INT, Funvotes INT, ID INT PRIMARY KEY)""")

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
    
    # Commit the transaction and close the connection
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

def load_datalake(data,response_image,name, APP_ID):

    data_lake_dir = 'datalake'
    if not os.path.exists(data_lake_dir):
        os.makedirs(data_lake_dir)
    conn = sqlite3.connect('steam_games_info.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datalake_metadata (
            APP_ID INTEGER PRIMARY KEY,
            Name TEXT,
            json_name TEXT,
            json_size INTEGER,
            image_name TEXT,
            image_size INTEGER,
            json_created_at TEXT,
            json_modified_at TEXT,
            image_created_at TEXT,
            image_modified_at TEXT
        )
    ''')

# Function to store raw data and image
    file_path = os.path.join(data_lake_dir, APP_ID+".json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    if "Content-Type" in response_image.headers:
        content_type = response_image.headers["Content-Type"]
        if content_type.startswith("image/"):
            ext = "." + content_type.split("/")[-1]  # Extract extension 
    
    file_path_img = os.path.join(data_lake_dir, APP_ID+"_header"+ext)
    with open(file_path_img, "wb") as file:  # Open in binary write mode
            for chunk in response_image.iter_content(1024):  # Read in chunks
                file.write(chunk)
    print(f"Image saved as {file_path}")

    
# Function to store metadata
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_name_img = os.path.basename(file_path_img)
    file_size_img = os.path.getsize(file_path_img)

    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_path)))
    modified_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
    created_at_img = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_path_img)))
    modified_at_img = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path_img)))
  
    cursor.execute('''
        INSERT or replace INTO datalake_metadata (APP_ID, Name, json_name, json_size, json_created_at, json_modified_at, image_name, image_size, image_created_at, image_modified_at)
        VALUES (?, ?, ?, ?, ?, ?,?,?,?,?)
    ''', (APP_ID, name, file_name, file_size, created_at, modified_at, file_name_img, file_size_img, created_at_img, modified_at_img))

    conn.commit()



