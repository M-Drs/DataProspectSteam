import subprocess, os
from pathlib import Path
from dotenv import load_dotenv

def uploadToServer():
# Define source and destination
    load_dotenv()
    local_path = str(Path("steam_games_info.db").resolve())
    remote_user = os.getenv("REMOTE_USER")
    remote_host = os.getenv("REMOTE_HOST")
    remote_path = os.getenv("REMOTE_PATH")
    port = os.getenv("PORT")

    # Build secure copy protocol command
    scp_command = [
        "scp",
        "-P", port,
        local_path,
        f"{remote_user}@{remote_host}:{remote_path}"
    ]

    # Run it
    try:
        subprocess.run(scp_command, check=True)
        print("Transfer successful!")
    except subprocess.CalledProcessError as e:
        print(f"SCP failed: {e}")
