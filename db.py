import psycopg2

def db_connection():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='Chirpers',
        user='postgres',
        password='20072004'
    )
    return conn
