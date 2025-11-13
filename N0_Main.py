from N1_Call_API import get_steam_details, get_steam_review_score, get_steam_all_reviews, get_image 
from N2_Insert_BDD import insert_games_in_database, load_datalake, insert_game_review_score 
from N3_Data_Upload import uploadToServer; from N9_DBviewer import last_max_id,liste_App_ID
import time, random


if __name__ == "__main__":
    
    i = last_max_id()
    while i < 9000:
        Resultat = get_steam_details(i)

        if "Error: API request failed" in Resultat:  
            time.sleep(random.uniform(10,15))
            i -= 1
        elif Resultat["Code_retour"] == False : 
            insert_games_in_database(Resultat)

        elif Resultat["Code_retour"] == True :
            insert_games_in_database(Resultat)
            image=get_image(Resultat["Url_image"])
            load_datalake(image, Resultat)

            insert_game_review_score(i, get_steam_review_score(i))

        i += 1
        time.sleep(random.uniform(0.5,1))

    for APP_ID,steam_cursor in (liste_ID := liste_App_ID()) :
        get_steam_all_reviews(APP_ID,steam_cursor)

    uploadToServer()
