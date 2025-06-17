#comment lancer ce fichier?
# sudo mkdir /home/break/work/my_fastapi_project
# cd /home/break/work/my_fastapi_project
# sudo python3 -m venv venv
# pip install fastapi uvicorn  
# ==========================
# puis, à relancer à chaque fois
# source venv/bin/activate
# nohup uvicorn N7_Rest_API:app --reload --host 0.0.0.0  --port 8000 > output.log 2>&1 &   

import os,random, sqlite3 
# import aiofiles
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



@app.get("/ip")
def get_ip(request: Request):
    client_host = request.client.host
    return {"ip": client_host}

@app.get ("/games")  #http://127.0.0.1:8000/games
def read_games():

    conn = sqlite3.connect("steam_games_info.db")
    cursor = conn.cursor()

    try : cursor.execute("""select game, release_date, price from games where Game is not null order by 1 asc ;""") 
    except Exception as e : 
        print(e)
        return "error"

    liste_game = [k for k in cursor.fetchall()]
    conn.close()

    return liste_game




@app.get("/items/{item_id}")             #on y accède donc par /items/450?q=lol
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/menu")
def menu():

    directory_path = "/home/break/disques/ssd2/Videos"
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
        
        
# @app.get("/stream/{filename}")
# async def stream_video(filename: str, request: Request):
#     directory_path = "/home/break/disques/ssd2/Videos"
#     file_path = os.path.join(directory_path, filename)

#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     file_size = os.path.getsize(file_path)
#     range_header = request.headers.get("range")

#     start = 0
#     end = file_size - 1

#     if range_header:
#         # Example of range header: "bytes=0-1023"
#         bytes_range = range_header.strip().lower().replace("bytes=", "").split("-")
#         if bytes_range[0].isdigit():
#             start = int(bytes_range[0])
#         if len(bytes_range) == 2 and bytes_range[1].isdigit():
#             end = int(bytes_range[1])

#     # Validate range
#     if start > end or end >= file_size:
#         raise HTTPException(status_code=416, detail="Invalid range")

#     chunk_size = end - start + 1

#     async def iter_file():
#         async with aiofiles.open(file_path, "rb") as f:
#             await f.seek(start)
#             remaining = chunk_size
#             while remaining > 0:
#                 chunk = await f.read(min(4096, remaining))
#                 if not chunk:
#                     break
#                 remaining -= len(chunk)
#                 yield chunk

#     headers = {
#         "Content-Range": f"bytes {start}-{end}/{file_size}",
#         "Accept-Ranges": "bytes",
#         "Content-Length": str(chunk_size),
#         "Content-Type": "video/x-matroska",  # Adjust MIME type as needed, e.g. "video/webm"
#     }

#     return StreamingResponse(iter_file(), status_code=206 if range_header else 200, headers=headers)
