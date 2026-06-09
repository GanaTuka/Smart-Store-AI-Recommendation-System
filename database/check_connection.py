import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


REQUIRED_TABLES = [
    "category_translation",
    "customers",
    "sellers",
    "products",
    "orders",
    "order_items",
    "payments",
    "reviews",
]


def main():
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "smart_store")

    print("Checking MySQL settings...")
    print(f"MYSQL_HOST={host}")
    print(f"MYSQL_USER={user}")
    print(f"MYSQL_DATABASE={database}")
    print(f"MYSQL_PASSWORD={'set' if password else 'empty'}")

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
    except mysql.connector.Error as error:
        print("\nFAILED: Cannot log in to MySQL.")
        print(f"MySQL error: {error}")
        print("\nFix: start MySQL and correct MYSQL_USER/MYSQL_PASSWORD in .env.")
        return

    print("\nOK: MySQL login works.")
    cursor = connection.cursor()

    cursor.execute("SHOW DATABASES LIKE %s", (database,))
    if not cursor.fetchone():
        print(f"\nFAILED: Database '{database}' does not exist.")
        print("Fix: run `mysql -u root -p < database/schema.sql`.")
        cursor.close()
        connection.close()
        return

    print(f"OK: Database '{database}' exists.")
    cursor.execute(f"USE `{database}`")

    missing_tables = []
    empty_tables = []
    for table in REQUIRED_TABLES:
        cursor.execute("SHOW TABLES LIKE %s", (table,))
        if not cursor.fetchone():
            missing_tables.append(table)
            continue

        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        print(f"OK: {table}: {count} rows")
        if count == 0:
            empty_tables.append(table)

    cursor.close()
    connection.close()

    if missing_tables:
        print(f"\nFAILED: Missing tables: {', '.join(missing_tables)}")
        print("Fix: rerun `mysql -u root -p < database/schema.sql`.")
        return

    if empty_tables:
        print(f"\nFAILED: Empty tables: {', '.join(empty_tables)}")
        print("Fix: run `python -m database.import_data`.")
        return

    print("\nSUCCESS: MySQL is configured and Olist data is loaded.")


if __name__ == "__main__":
    main()
