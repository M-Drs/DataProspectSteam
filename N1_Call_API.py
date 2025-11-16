import requests, time, random
from N2_Insert_BDD import insert_review_in_database, insert_last_cursor_position


def get_steam_details(APP_ID):
    
    APP_ID = str(APP_ID)
    URL = f"https://store.steampowered.com/api/appdetails?appids={APP_ID}" 

    try : response = requests.get(URL) ; response.encoding = 'utf-8-sig'
    except Exception as e: input(f"Request failed for {APP_ID}: {e},press enter to retry") ; return None

    if response.status_code != 200 or not response.text.strip() or ("json" not in (response.headers.get("Content-Type", "").lower())):
        print("Error APP_ID:",APP_ID,"Status:",response.status_code,"Content-Type:",response.headers.get("Content-Type"),"Raw text:", response.text[:50])
        return None
    
    data=response.json()
    if data[APP_ID]["success"] == False :
        return {"APP_ID":APP_ID,"Game":None,"Code_retour":False }
    
    info=data[APP_ID]["data"] ; name=info["name"] ; url_image=info["header_image"] ; release_date=info["release_date"]["date"] ; price=info["price_overview"]["final_formatted"] if "price_overview" in info else None ; gratuit=info["is_free"] 
    platforms=[k for k, v in info["platforms"].items() if v] ; genres=[genre["description"] for genre in info.get("genres",[])] ; detailed_description=info["detailed_description"] ; supported_languages=info.get("supported_languages") ; metacritic_score=info.get("metacritic",{}).get("score") ; metacritic_url=info.get("metacritic",{}).get("url") ; print(f"\nGame: {name}\nRelease Date: {release_date}\nPrice: {price}\nGenres: {' | '.join(genres)}\nHeader_image: {url_image}\nAvailable on: {' | '.join(platforms)}\nmetacritic_score: {metacritic_score}\nmetacritic_url: {metacritic_url}")
    return {"Code_retour":True, "Full_reponse":response, "Data":data, "APP_ID":APP_ID,"Game":name, "Release_Date":release_date, "Price":price, "Gratuit":gratuit, "Genres":' | '.join(genres), "Detailed_description":detailed_description, "Url_image":url_image, "Supported_languages":supported_languages, "Platforms":' | '.join(platforms), "Metacritic_score":metacritic_score, "Metacritic_url":metacritic_url}

def get_image(url_image):
    if url_image is not None :
        response_image = requests.get(url_image, stream=True)  # Stream to handle large files
        print(f"Img fetch : {response_image}")
        return(response_image)
    
def get_steam_review_score(APP_ID): 
    
    BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"
    PARAMS = {"json": 1,
        "language": "all",  
        "review_type": "all",  
        "cursor": "*"} 
    
    response = requests.get(BASE_URL, params=PARAMS)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return (f"Error: Received status code {response.status_code}")

    data = response.json()
    query_summary = data.get("query_summary","")
    return (query_summary)
    
def get_steam_all_reviews(APP_ID,steam_cursor="*"):
    
    BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"
    PARAMS = {
        "json": 1,
        "filter": "recent",  # Can be "all", "recent", or "updated"
        "language": "all",  
        "review_type": "all",  
        "num_per_page": 100,
        "cursor": steam_cursor }
    i=1
    print(steam_cursor)
    while i < 10 :
        i += 1
        response = requests.get(BASE_URL, params=PARAMS)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            time.sleep(random.uniform(10,15))

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



if __name__ == "__main__":
    #reviews = fetch_reviews(570)
    #print(reviews)
    get_steam_details(570)

    