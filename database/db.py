import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


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
