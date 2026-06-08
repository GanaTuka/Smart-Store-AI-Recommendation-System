import os
<<<<<<< HEAD
from sqlalchemy import create_engine
=======
from contextlib import contextmanager

import mysql.connector
>>>>>>> 9708887a48e63c3eb385b09d3af6be2e1ad337fb
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "smart_store")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)
=======

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "smart_store_ai"),
    )


@contextmanager
def db_cursor(dictionary=True):
    connection = get_connection()
    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def fetch_all(query, params=None):
    with db_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()


def get_products():
    return fetch_all("SELECT * FROM products ORDER BY id")


def get_users():
    return fetch_all("SELECT * FROM users ORDER BY id")


def get_orders():
    return fetch_all("SELECT * FROM orders ORDER BY order_date DESC")
>>>>>>> 9708887a48e63c3eb385b09d3af6be2e1ad337fb
