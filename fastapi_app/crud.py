from database import get_connection  
print("Connecting to the database...")

def get_channels():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
                SET search_path TO raw; 
                SELECT channel_name, COUNT(*) AS message_count
                FROM telegram_messages
                GROUP BY channel_name
                ORDER BY message_count DESC;
                """)    
    results = cur.fetchall()
    print("results:", results)
    conn.close()

    return {"products": results}

def get_products():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
                SET search_path TO raw; 
                SELECT detected_object_class, COUNT(detected_object_class) AS objects
                FROM yolo_detections
                GROUP BY detected_object_class
                """)    
    results = cur.fetchall()
    print("results:", results)
    conn.close()

    return {"products": results}