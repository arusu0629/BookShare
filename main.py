import os
from datetime import datetime

from notion_client import Client
from get_notion_info import get_database_data, download_image, get_database_id
from post_instagram import login_instagram, post_to_instagram
from dotenv import load_dotenv
from pprint import pprint

# 環境変数の読み込み
load_dotenv()

# Notion クライアント作成
notion_client = Client(auth=os.environ["NOTION_API_KEY"])

# Instagramにログイン
INSTAGRAM_USERNAME = os.environ["INSTAGRAM_USERNAME"]
INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]

api = login_instagram(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

def mark_as_posted(page_id):
    page = notion_client.pages.retrieve(page_id)
    notion_client.pages.update(
        page_id,
        properties={
            "投稿済み": {
                "checkbox": True
            }
        }
    )

def filter_data_for_today(database_data):
    today = datetime.today().date()
    filtered_data = []

    for data in database_data:
        scheduled_date_str = data["scheduled_date"]["start"]
        scheduled_date = datetime.strptime(scheduled_date_str, "%Y-%m-%d").date()

        if scheduled_date == today and not data["posted"]:
            filtered_data.append(data)

    return filtered_data

if __name__ == "__main__":
    # Notionからデータを取得
    database_id = get_database_id(os.environ["NOTION_DATABASE_URL"])
    database_data = get_database_data(database_id)

    # 今日の投稿データを抽出
    filtered_data = filter_data_for_today(database_data)

    for data in filtered_data:
        # 画像をダウンロード
        image_paths = [download_image(image["file"]["url"]) for image in data["images"]]
        
        # Instagramへ投稿
        post_to_instagram(api, data["description"], data["hashtags"], image_paths)

        # 投稿が成功したら投稿済みにチェックを入れる
        mark_as_posted(data["id"])

        # ダウンロードした画像を破棄する
        for image_path in image_paths:
            os.remove(image_path)