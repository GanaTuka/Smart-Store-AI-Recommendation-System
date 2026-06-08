from database.db import fetch_all


def get_sales_summary():
    rows = fetch_all(
        """
        SELECT SUM(o.quantity * p.price) AS total_sales, COUNT(*) AS total_orders
        FROM orders o
        JOIN products p ON p.id = o.product_id
        """
    )
    return rows[0] if rows else {"total_sales": 0, "total_orders": 0}
