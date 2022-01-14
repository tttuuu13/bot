from re import L
import psycopg2
from config import host, user, password, db_name
from PIL import Image


def add(name, description, image):
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
                """INSERT INTO formulas (name, description, image)
                VALUES (%s, %s, %s)""",
                (name, description, image)
            )
        return True
        
    except Exception as e:
        return f"ошибка с базой данных: {e}"
    finally:
        if connection:
            connection.close()

def get_by_index(index):
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
                """SELECT * FROM formulas LIMIT %s OFFSET %s;""",
                (index+1, index)
            )
            r = cursor.fetchone()
            if r[2] != None:
                r = r[:2] + (bytes(r[2]),)
            return r
    except Exception as e:
        print(f"[INFO] ошибка с базой данных: {e}")
    finally:
        if connection:
            connection.close()


def get_names():
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
                """SELECT name FROM formulas;""",
            )
            r = []
            for tuple in cursor.fetchall():
                r.append(tuple[0])
            return r
    except Exception as e:
        print(f"[INFO] ошибка с базой данных: {e}")
    finally:
        if connection:
            connection.close()

def delete_row(index):
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
                """DELETE FROM formulas LIMIT %s OFFSET %s;""",
                (index+1, index)
            )
            return True
    except Exception as e:
        print(f"[INFO] ошибка с базой данных: {e}")
    finally:
        if connection:
            connection.close()

def clear_db():
    try:
        return # ЗАЩИТА
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        
        connection.autocommit = True
        
        with connection.cursor() as cursor:
            cursor.execute(
                """TRUNCATE formulas;
                   DELETE FROM formulas;""",
            )
            return True
    except Exception as e:
        print(f"[INFO] ошибка с базой данных: {e}")
    finally:
        if connection:
            connection.close()

def other(request):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        
        connection.autocommit = True
        
        with connection.cursor() as cursor:
            cursor.execute(request)
        return cursor.fetchall()
    except Exception as e:
        print(f"[INFO] ошибка с базой данных: {e}")
    finally:
        if connection:
            connection.close()
