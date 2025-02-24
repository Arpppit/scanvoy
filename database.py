import psycopg2
from datetime import datetime

conn = None 


def get_connector():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5437"
        )
    return conn 
    

def insert_into_db(html_content):
    conn = get_connector()
    cursor = conn.cursor()
    timestamp = datetime.now()

    insert_query = """
    INSERT INTO htmldata (timestamp, html_content)
    VALUES (%s, %s);
    """
    cursor.execute(insert_query, (timestamp, html_content))
    conn.commit()
    cursor.close()
    conn.close()
    print("data inserted.")

    


def get_data_from_db(interval):
    conn = get_connector()
    cursor = conn.cursor()

    # Query HTML data from the last 15 minutes
    query = f"""
    SELECT * 
    FROM HtmlData
    WHERE timestamp >= NOW() - INTERVAL '{interval}';
    """
    cursor.execute(query)

    # Fetch results
    rows = cursor.fetchall()
    print(len(rows))

    cursor.close()
    conn.close()
    return rows