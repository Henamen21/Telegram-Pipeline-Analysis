import os
import json
import glob
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

DATA_FOLDER = "data/raw/telegram_messages"

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def load_json_to_postgres():
    conn = connect_db()
    cur = conn.cursor()

    for date_folder in os.listdir(DATA_FOLDER):
        folder_path = os.path.join(DATA_FOLDER, date_folder)
        for json_file in glob.glob(os.path.join(folder_path, "*.json")):
            channel_name = os.path.splitext(os.path.basename(json_file))[0]
            with open(json_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    cur.execute("""
                        INSERT INTO raw.telegram_messages (
                            id, channel_name, message_date, sender_id,
                            message_text, has_media, media_path
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        msg.get("id"),
                        channel_name,
                        msg.get("date"),
                        msg.get("sender_id"),
                        msg.get("text"),
                        msg.get("has_media"),
                        msg.get("media_path")
                    ))
            print(f"Loaded: {json_file}")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_json_to_postgres()
