from instagrapi import Client
from dotenv import load_dotenv
import os

# JSON ファイルの名前
JSON_FILE = "session.json"

def login_instagram(username, password):
    client = Client()
    if os.path.exists(JSON_FILE):
        print("Found session file.")
        client.load_settings(JSON_FILE)
        client.login(username, password)
    else:
        print("Session file not found.")
        client.login(username, password)
        client.dump_settings(JSON_FILE)

    return client

def post_to_instagram(api, description, hashtags, image_paths):
    caption = f"{description}\n{hashtags}"
    media = [image_path for image_path in image_paths]
    api.album_upload(media, caption=caption)
