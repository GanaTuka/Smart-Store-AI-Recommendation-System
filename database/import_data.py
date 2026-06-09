from pathlib import Path

import pandas as pd

from database.db import engine


BASE_DIR = Path(__file__).resolve().parent.parent

FILES = {
    "category_translation": "product_category_name_translation.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}


def import_dataset():
    for table, filename in FILES.items():
        path = BASE_DIR / "dataset" / filename
        print(f"Importing {table} from {path}...")
        dataframe = pd.read_csv(path)
        dataframe.to_sql(table, engine, if_exists="append", index=False)
        print(f"{table} imported: {len(dataframe)} rows")

    print("All Olist data imported successfully.")


if __name__ == "__main__":
    import_dataset()
