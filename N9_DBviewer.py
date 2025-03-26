import sqlite3


def last_max_id():
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try : cursor.execute("""select max(APP_ID) from games limit 1;""") 
    except : return 1

    max_id = cursor.fetchone()[0]
    conn.close()

    if max_id is None : return 1
    return max_id

# rows = cursor.fetchall()
# for row in rows:
#     print(row)
# conn.close()

def liste_App_ID():
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try : cursor.execute("""select APP_ID,Last_cursor_position from games where Game is not null order by 1 asc ;""") 
    except : return 1

    liste_id = [k for k in cursor.fetchall()]
    conn.close()

    print(liste_id)
    if liste_id is None : return 1
    return liste_id

if __name__ == "__main__":

    print(last_max_id())
    print(liste_App_ID())

    # conn = sqlite3.connect("steam_games_info.db")
    # cursor = conn.cursor()
    # n= 790
    # while n < 830 :
    #     cursor.execute(f"""delete from games where APP_ID = {n};""") 
    #     n+=1
    # conn.commit()    
    # conn.close()
