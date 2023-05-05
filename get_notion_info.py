from notion_client import Client
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse

# 環境変数の読み込み
load_dotenv()

notion = Client(auth=os.environ["NOTION_API_KEY"])

# データベースのURLからデータベースIDを返す
def get_database_id(database_url):
    database_id = database_url.split("/")[-1].split("?")[0]
    return database_id

# データベースにあるデータを返す
def get_database_data(database_id):
    database_data = []
    results = notion.databases.query(database_id).get("results")
    for result in results:
        data = {
            "id": result["id"],
            "description": result["properties"]["説明文"]["rich_text"][0]["plain_text"] if result["properties"]["説明文"]["rich_text"] else "",
            "hashtags": result["properties"]["ハッシュタグ"]["rich_text"][0]["plain_text"] if result["properties"]["ハッシュタグ"]["rich_text"] else "",
            "images": result["properties"]["画像"]["files"],
            "scheduled_date": result["properties"]["投稿予定日"]["date"],
            "posted": result["properties"]["投稿済み"]["checkbox"],
        }
        database_data.append(data)
    return database_data

def download_image(url):
    response = requests.get(url)
    image_name = os.path.basename(urlparse(url).path)
    with open(image_name, "wb") as f:
        f.write(response.content)
    return image_name