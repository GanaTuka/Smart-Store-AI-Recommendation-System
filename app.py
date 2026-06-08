<<<<<<< HEAD
# from flask import Flask, render_template
# from routes.analytics import analytics_bp
# from routes.auth import auth_bp
# from routes.products import products_bp
# from routes.recommendations import recommendations_bp


# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "hackathon-secret-key"

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(products_bp)
#     app.register_blueprint(recommendations_bp)
#     app.register_blueprint(analytics_bp)

#     @app.route("/")
#     def home():
#         return render_template("dashboard.html")

#     return app


# app = create_app()


# if __name__ == "__main__":
#     app.run(debug=True)


import pandas as pd
from database.db import engine

files = {
    "category_translation": "dataset/product_category_name_translation.csv",
    "customers": "dataset/olist_customers_dataset.csv",
    "sellers": "dataset/olist_sellers_dataset.csv",
    "products": "dataset/olist_products_dataset.csv",
    "orders": "dataset/olist_orders_dataset.csv",
    "order_items": "dataset/olist_order_items_dataset.csv",
    "payments": "dataset/olist_order_payments_dataset.csv",
    "reviews": "dataset/olist_order_reviews_dataset.csv",
}

for table, path in files.items():
    print(f"Importing {table}...")
    df = pd.read_csv(path)
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"{table} done")

print("All data imported successfully.")
=======
from flask import Flask, render_template
from routes.analytics import analytics_bp
from routes.auth import auth_bp
from routes.products import products_bp
from routes.recommendations import recommendations_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hackathon-secret-key"

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(analytics_bp)

    @app.route("/")
    def home():
        return render_template("dashboard.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 9708887a48e63c3eb385b09d3af6be2e1ad337fb
