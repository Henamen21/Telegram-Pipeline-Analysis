import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data//raw//yolo_detections.csv")  # Or your in-memory df

# PostgreSQL connection info
user = "myuser"
password = "mypassword"
host = "localhost"          # or "127.0.0.1" or Docker container name
port = "5432"
database = "telegram_db"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

# Load DataFrame to raw.yolo_detections
df.to_sql("yolo_detections", engine, schema="raw", if_exists="replace", index=False)

print("✅ DataFrame successfully written to raw.yolo_detections!")
