import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_database_name():
    return os.getenv("MYSQL_DATABASE", "smart_store")


def get_connection(database=None):
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=database or get_database_name(),
    )


def get_engine():
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "localhost")
    database = get_database_name()
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4")


engine = get_engine()


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


def get_products(limit=30):
    return fetch_all(
        """
        SELECT
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm,
            ROUND(AVG(oi.price), 2) AS avg_price,
            COUNT(oi.order_id) AS times_sold
        FROM products p
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        LEFT JOIN order_items oi
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            category,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm
        ORDER BY times_sold DESC, avg_price DESC
        LIMIT %s
        """,
        (limit,),
    )


def get_customers(limit=20):
    return fetch_all(
        """
        SELECT customer_id, customer_unique_id, customer_city, customer_state
        FROM customers
        ORDER BY customer_state, customer_city
        LIMIT %s
        """,
        (limit,),
    )


def get_orders(limit=30):
    return fetch_all(
        """
        SELECT order_id, customer_id, order_status, order_purchase_timestamp
        FROM orders
        ORDER BY order_purchase_timestamp DESC
        LIMIT %s
        """,
        (limit,),
    )
