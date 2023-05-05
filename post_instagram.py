from instagrapi import Client
from dotenv import load_dotenv
import os

def login_instagram(username, password):
    api = Client()
    api.login(username, password)
    return api

def post_to_instagram(api, description, hashtags, image_paths):
    caption = f"{description}\n{hashtags}"
    media = [image_path for image_path in image_paths]
    api.album_upload(media, caption=caption)
