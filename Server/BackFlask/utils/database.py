import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_CONNECTION_PORT = os.getenv("POSTGRES_CONNECTION_PORT")
POSTGRES_ARTICLES = os.getenv("POSTGRES_ARTICLES")
POSTGRES_USERS = os.getenv("POSTGRES_USERS")

articles_connection = ("host='%s' \
        dbname='%s' \
        user='%s' \
        password='%s' \
        port='%s'"
           % (POSTGRES_DATABASE_URL,
              POSTGRES_ARTICLES,
              POSTGRES_USERNAME,
              POSTGRES_PASSWORD,
              POSTGRES_CONNECTION_PORT))

users_connection = ("host='%s' \
        dbname='%s' \
        user='%s' \
        password='%s' \
        port='%s'"
           % (POSTGRES_DATABASE_URL,
              POSTGRES_USERS,
              POSTGRES_USERNAME,
              POSTGRES_PASSWORD,
              POSTGRES_CONNECTION_PORT))