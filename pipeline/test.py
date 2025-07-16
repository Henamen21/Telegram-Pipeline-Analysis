from ultralytics import YOLO
from pathlib import Path
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DB connection params
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# Paths
IMAGE_DIR = Path("D:/Project/10 Academy Resourse/week 7/Telegram-Pipeline-Analysis/data/raw/media")

# Load YOLO model
model = YOLO("yolov8n.pt")

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def get_existing_message_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT message_id FROM raw.yolo_detections;")
    rows = cur.fetchall()
    cur.close()
    return set(str(row[0]) for row in rows)

def insert_detections(conn, records):
    cur = conn.cursor()
    for r in records:
        cur.execute("""
            INSERT INTO raw.yolo_detections (message_id, detected_object_class, confidence_score)
            VALUES (%s, %s, %s)
        """, (r["message_id"], r["detected_object_class"], r["confidence_score"]))
    conn.commit()
    cur.close()


def run_yolo_on_images(image_dir: Path):
    print(f"📂 Scanning images in: {image_dir.resolve()}")

    if not image_dir.exists():
        print("❌ Image directory not found.")
        return

    conn = connect_db()
    processed_ids = get_existing_message_ids(conn)
    print(f"🔁 Skipping {len(processed_ids)} already processed message_ids.")

    records = []

    for image_path in image_dir.glob("*.jpg"):
        message_id = image_path.stem
        if message_id in processed_ids:
            print(f"⏭️ Skipping {message_id}")
            continue

        print(f"🔍 Processing {image_path.name}")
        results = model(image_path)

        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]

                records.append({
                    "message_id": message_id,
                    "detected_object_class": class_name,
                    "confidence_score": confidence
                })
                print(f"✅ {class_name} ({confidence:.2f}) in {message_id}")

    if records:
        insert_detections(conn, records)
        print(f"✅ Inserted {len(records)} new detections into Postgres.")
    else:
        print("✅ No new detections to add.")

    conn.close()

# Run
if __name__ == "__main__":
    run_yolo_on_images(IMAGE_DIR)