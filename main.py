import os,random
#import requests  importer le package
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

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