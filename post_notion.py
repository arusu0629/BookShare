from notion_client import Client
import os
import datetime
import glob
import sys
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Notion API クライアントを作成
notion = Client(auth=os.environ["NOTION_API_KEY"])

# データベースの ID を取得
database_id = os.environ["NOTION_DATABASE_ID"]

def create_page(name, description, hashtags, post_date, posted):
    new_page = {
        "名前": {"title": [{"text": {"content": name}}]},
        "説明文": {"rich_text": [{"text": {"content": description}}]},
        "ハッシュタグ": {"rich_text": [{"text": {"content": hashtags}}]},
        "投稿予定日": {"date": {"start": post_date.isoformat()}},
        "投稿済み": {"checkbox": posted},
    }

    return new_page

def add_page_to_database(name, description, hashtags, post_date, posted):
    new_page = create_page(name, description, hashtags, post_date, posted)
    notion.pages.create(parent={"database_id": database_id}, properties=new_page)

# 指定されたフォルダパスからファイルを読み込む
def read_file(file_name):
    # フォルダーパスを取得する
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return content

name = read_file("title.txt")
description = read_file("description.txt")
hashtags = read_file("hashtag.txt")
post_date = datetime.datetime.strptime(read_file("date.txt"), "%Y-%m-%d").date()
posted = False

# 画像ファイルを探す(※NotionAPIでプロパティへの複数枚画像のアップロードは出来ない)
# uploaded_image_urls = read_file("images_url.txt")

# 情報を Notion データベースに追加
add_page_to_database(name, description, hashtags, post_date, posted)