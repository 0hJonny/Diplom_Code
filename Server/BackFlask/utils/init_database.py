import psycopg2
from utils.database import connection, initialize_database


def init_db() -> bool:
    with connection, connection.cursor() as cursor:
        try:
            initialize_database(cursor)  # Инициализация таблиц при необходимости
            connection.commit()
        except psycopg2.Error as err:
            print(f"Error initializing the database: {err}")
            return False
        return True


def run() -> bool:
    return init_db()
