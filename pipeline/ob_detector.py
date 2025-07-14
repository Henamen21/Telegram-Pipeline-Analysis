from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # or yolov8m.pt, yolov8s.pt, etc.

import os
import pandas as pd
from ultralytics import YOLO
from pathlib import Path

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Path to scraped images (adjust accordingly)
IMAGE_DIR = Path("..//data//raw//media//")

# Placeholder for results
records = []

# Load already processed message_ids
existing_ids = set()
csv_path = Path("..//data//raw//yolo_detections.csv")

if csv_path.exists():
    existing_df = pd.read_csv(csv_path)
    existing_ids = set(existing_df["message_id"].astype(str))

print(f"Skipping {len(existing_ids)} already processed images.")

for image_path in IMAGE_DIR.glob("*.jpg"):  # Adjust extensions if needed
    # Extract message_id from filename (e.g., "12345.jpg" → 12345)
    
    try:
        message_id = image_path.stem

        if message_id in existing_ids:
            continue  # ✅ Skip already processed images
        
        results = model(image_path)
        print(f"Processing {image_path} with message_id: {message_id}")
        for r in results:
            boxes = r.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]
                
                records.append({
                    "message_id": message_id,
                    "detected_object_class": class_name,
                    "confidence_score": confidence
                })
                print(f"Detected {class_name} with confidence {confidence:.2f} in message {message_id}")
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")

new_df = pd.DataFrame(records)

if csv_path.exists():
    new_df.to_csv(csv_path, mode='a', header=False, index=False)  # append
else:
    new_df.to_csv(csv_path, index=False)

