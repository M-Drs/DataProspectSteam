from N1_Call_API import get_steam_details, get_steam_review_score ; from N2_Insert_BDD import insert_games_in_database, insert_game_review_score
import time, random
 
if __name__ == "__main__":
 
    

    i = 10131
    while i < 99999:
        Resultat= get_steam_details(i)

        if "Error: API request failed" in Resultat:  # Check if 'Error' is in the return string
            delay = random.uniform(10,15)
            time.sleep(delay)
            i -= 1

        elif Resultat["Code_retour"] == True :
        # SEND THIS JSON Resultat["Full_reponse"]
            insert_games_in_database(Resultat)

            review_score_general = get_steam_review_score(i)
            insert_game_review_score()

        i += 1
        delay = random.uniform(0.3,1)
        time.sleep(delay)

        
