import os
import json
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}
print(DB_PARAMS["dbname"], DB_PARAMS["user"], DB_PARAMS["host"], DB_PARAMS["port"])

DATA_FOLDER = Path("data/raw/telegram_messages")

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def load_all_jsons_to_postgres():
    conn = connect_db()
    cur = conn.cursor()

    if not DATA_FOLDER.exists():
        print("❌ No data folder found.")
        return

    for date_folder in DATA_FOLDER.iterdir():
        if not date_folder.is_dir():
            continue

        print(f"📁 Processing folder: {date_folder.name}")
        
        for json_file in date_folder.glob("*.json"):
            channel_name = json_file.stem
            with open(json_file, "r", encoding="utf-8") as f:
                messages = json.load(f)

                

                for msg in messages:

                    if not msg.get("id"):
                        print(f"⚠️ Skipping message without ID: {msg}")
                        continue

                    cur.execute("""
                        SELECT 1 FROM raw.telegram_messages
                        WHERE message_id = %s AND channel_name = %s
                    """, (msg.get("id"), channel_name))
                    
                    if cur.fetchone():
                        continue  # Already exists

                    cur.execute("""
                        INSERT INTO raw.telegram_messages (
                            message_id, channel_name, message_date,
                            message_text, has_media, media_path
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        msg.get("id"),
                        channel_name,
                        msg.get("date"),
                        msg.get("text"),
                        msg.get("has_media"),
                        msg.get("media_path")
                    ))

            print(f"✅ Loaded: {json_file.name}")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All messages loaded into Postgres.")

if __name__ == "__main__":
    load_all_jsons_to_postgres()
