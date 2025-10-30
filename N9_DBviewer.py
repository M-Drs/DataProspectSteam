import sqlite3


def last_max_id():
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try : cursor.execute("""select max(APP_ID) from games limit 1;""") 
    except Exception as e : 
        print(e)
        return 1

    max_id = cursor.fetchone()[0]
    conn.close()

    if max_id is None : return 1
    return max_id

def liste_App_ID():
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try : cursor.execute("""select APP_ID,Last_cursor_position from games where Game is not null order by 1 asc ;""") 
    except Exception as e : 
        print(e)
        return [(10,None)]

    liste_id = [k for k in cursor.fetchall()]
    conn.close()

    print(liste_id)
    if liste_id is None : return [(10,None)]
    return liste_id



def custom_query():
    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT COUNT(*) FROM (SELECT DISTINCT ID FROM reviews);""")
        resultats = cursor.fetchall()
        
        # Récupère les noms de colonnes
        colonnes = [description[0] for description in cursor.description]

        # Affiche les noms de colonnes
        print("\t".join(colonnes))
        print("-" * 60)

        # Affiche chaque ligne
        for ligne in resultats:
            print("\t".join(str(x) for x in ligne))

    except Exception as e:
        print("Erreur SQL :", e)

    finally:
        conn.close()

if __name__ == "__main__":



    custom_query()


    # conn = sqlite3.connect("steam_games_info.db")
    # cursor = conn.cursor()
    # while n:= 790 < 830 :
    #     cursor.execute(f"""delete from games where APP_ID = {n};""") 
    #     n+=1
    # conn.commit()    
    # conn.close()

#requête pour trouver quel jeux n'ont pas leur photo dans le datalake!!!!!!!!!!