import json
import psycopg2
from datetime import datetime
import os
from db import get_connection  



# --- List your JSON files ---
json_files = [
    "data\\raw\\telegram_messages\\2025-07-09\\lobelia4cosmetics.json",
    "data\\raw\\telegram_messages\\2025-07-09\\tikvahpharma.json"
]

# --- Start connection ---
conn = get_connection()
cur = conn.cursor()

print("connected")

for file_path in json_files:
    channel_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"✅ Channel '{channel_name}' is used")

    print(f"📂 Loading: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f'file {file_path} started')

    for msg in data:
        message_id = msg.get("id")
        message_date = msg.get("date")
        message_text = msg.get("text", "")
        channel_name = channel_name
        json_data = json.dumps(msg)  # Store full JSON in column

        # Parse date safely
        try:
            message_date = datetime.fromisoformat(message_date.replace("Z", "+00:00"))
        except Exception:
            message_date = None

        cur.execute("""
            INSERT INTO raw.telegram_messages (
                message_id, channel_name, message_date, message_text, json_data
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (message_id) DO NOTHING;
        """, (message_id, channel_name, message_date, str(message_text), json_data))

conn.commit()
cur.close()
conn.close()

print("✅ All files inserted successfully.")
