import requests, time
from N2_Insert_BDD import load_datalake, insert_review_in_database, insert_last_cursor_position


def get_steam_details(APP_ID):
    
    APP_ID = str(APP_ID)
    URL = f"https://store.steampowered.com/api/appdetails?appids={APP_ID}"
    response = requests.get(URL)
    data = response.json()

    if response.status_code != 200 or not response.text.strip():
        print(f"Error: API request failed or returned empty response for {APP_ID}")
        return f"Error: API request failed or returned empty response for {APP_ID}"

    if data[APP_ID]["success"] == False :
        #print(f"ID not found : {APP_ID}")
        return {"Code_retour" : False,"APP_ID": APP_ID,"Game": None }
    
    info = data[APP_ID]["data"]
    name = info["name"]
    header_image = info["header_image"]
    release_date = info["release_date"]["date"]
    price = info["price_overview"]["final_formatted"] if "price_overview" in info else None
    gratuit = info["is_free"]
    platforms = [k for k, v in info["platforms"].items() if v]
    genres = [genre["description"] for genre in info.get("genres",[])]
    detailed_description = info["detailed_description"]
    supported_languages = info.get("supported_languages") 
    metacritic_score = info.get("metacritic",{}).get("score") 
    metacritic_url = info.get("metacritic",{}).get("url") 

    response_image = requests.get(header_image, stream=True)  # Stream to handle large files
    if response_image.status_code == 200:
        load_datalake(data, response_image, name, APP_ID)
    else:
        return(f"Failed to download image. Status code: {response.status_code}")

    print(f"\nAPP_ID {APP_ID}\nGame: {name}\nRelease Date: {release_date}\nPrice: {price}\nGenres: {' | '.join(genres)}\nHeader_image: {header_image}\nAvailable on: {' | '.join(platforms)}\nmetacritic_score: {metacritic_score}\nmetacritic_url: {metacritic_url}")
    return {"Code_retour" : True,"Full_reponse" : response,"APP_ID": APP_ID,"Game": name,"Release_Date": release_date,"Price": price,"Gratuit": gratuit,"Genres": ' | '.join(genres),"Detailed_description": detailed_description,
            "Header_image": header_image,"Supported_languages": supported_languages,"Platforms": ' | '.join(platforms),"Metacritic_score": metacritic_score,"Metacritic_url": metacritic_url}

def get_steam_review_score(APP_ID):
    
    BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"
    PARAMS = {"json": 1,
        "language": "all",  # Change if needed
        "review_type": "all",  # "positive", "negative", or "all"
        "cursor": "*"}  # Initial cursor (Steam requires this format)
    
    response = requests.get(BASE_URL, params=PARAMS)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return (f"Error: Received status code {response.status_code}")

    data = response.json()
    query_summary = data.get("query_summary","")
    #print(query_summary["num_reviews"], query_summary["review_score"], query_summary["total_positive"], query_summary["total_negative"])
    return (query_summary)

    
def get_steam_all_reviews(APP_ID,steam_cursor="*"):
    
    BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"
    PARAMS = {
        "json": 1,
        "filter": "recent",  # Can be "all", "recent", or "updated"
        "language": "all",  # Change if needed
        "review_type": "all",  # "positive", "negative", or "all"
        "num_per_page": 100,
        "cursor": steam_cursor }
    
    print(steam_cursor)
    while True:
        response = requests.get(BASE_URL, params=PARAMS)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return (f"Error: Received status code {response.status_code}")

        data = response.json()
        reviews = data.get("reviews", [])

        print(steam_cursor := data.get("cursor", ""))
        # Update request parameters
        PARAMS["cursor"] = steam_cursor

        if  reviews == []:
            print("No more reviews available.")
            return
        else : 
            for review in reviews:
                insert_review_in_database(APP_ID,review)

        insert_last_cursor_position(APP_ID,steam_cursor)
        time.sleep(1.5)


        #if not reviews or not cursor: not steam_cursor or        
        # print(f"Positif: {review["voted_up"]}, Language: {review["language"]}, Votes_up: {review["votes_up"]}")
        # print(f"{'-'*50}\nUser: {review['author']['steamid']}, Playtime: {review['author']['playtime_forever']} mins, ID_review : {review['recommendationid']}, Language: {review["language"]}")
        # print(f"Review: {review['review']}")       
        

if __name__ == "__main__":
    #reviews = fetch_reviews(570)
    #print(reviews)
    get_steam_details(570)

    