#comment lancer ce fichier?
# sudo mkdir /home/break/work/my_fastapi_project
# cd /home/break/work/my_fastapi_project
# sudo python3 -m venv venv
# pip install fastapi uvicorn  
# ==========================
# puis, à relancer à chaque fois
# source venv/bin/activate
# nohup uvicorn main:app --reload --host 0.0.0.0 --host :: --port 8000 > output.log 2>&1 &   

import os,random, sqlite3
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get ("/games")  #http://127.0.0.1:8000/games
def read_games():

    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try : cursor.execute("""select game, release_date, price from games where Game is not null order by 1 asc ;""") 
    except Exception as e : 
        print(e)
        return f"error :\n {e}"

    liste_game = [k for k in cursor.fetchall()]
    conn.close()

    return liste_game




@app.get("/items/{item_id}")             #on y accède donc par /items/450?q=lol
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/menu")
def menu():

    directory_path = "/media/Disquessd2T/videos"
    files_info = {}

    try:
        # Walk through all directories and subdirectories
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_fake_review = random.choice(["This is the best thing since sliced bread!", "If I could give it more stars, I would!", "Bought this as a joke, ended up loving it!", "A game changer, literally changed my life!", "I laughed so hard, I cried... and then bought another one!","I'm Commander Shepard and this is my favorite movie on the Citadel."]) #requests.get("BASE_URL")
                files_info[file] = file_fake_review
        return {"status": "success", "files": files_info}
    
    


    except Exception as e:
        return {
            "status": "error",
            "type": str(e)
        }