import psycopg2
from db import get_connection  

conn = get_connection()
cur = conn.cursor()  # optional: return dicts instead of tuples

sql = """
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    json_data JSONB
);
"""

cur.execute(sql)
conn.commit()
cur.close()
conn.close()

print("Schema and table created!")
