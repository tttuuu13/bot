import psycopg2
from config import host, user, password, db_name


try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    
    connection.autocommit = True
    
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT nick"""
        )
    
except Exception as e:
    print("[INFO] Error while working with PostgreSQL", e)
finally:
    if connection:
        connection.close()
        print("[INFO] Connection closed")