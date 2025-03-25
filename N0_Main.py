from N1_Call_API import get_steam_details, get_steam_review_score ; from N2_Insert_BDD import insert_games_in_database, insert_game_review_score ; from N9_DBviewer import last_max_id
import time, random


def


if __name__ == "__main__":
    
    i = last_max_id()
    while i < 99999:
        Resultat = get_steam_details(i)
        if "Error: API request failed" in Resultat:  
            time.sleep(random.uniform(10,15))
            i -= 1
        elif Resultat["Code_retour"] == False :
            insert_games_in_database(Resultat)
        elif Resultat["Code_retour"] == True :
            insert_games_in_database(Resultat)
            review_score_general = get_steam_review_score(i)
            insert_game_review_score(i, review_score_general)
        i += 1
        time.sleep(random.uniform(0.3,1))

        
    