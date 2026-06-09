from database.db import fetch_all


def get_sales_summary():
    rows = fetch_all(
        """
        SELECT
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(*) AS total_items,
            ROUND(SUM(price), 2) AS total_sales
        FROM order_items
        """
    )
    return rows[0] if rows else {"total_orders": 0, "total_items": 0, "total_sales": 0}
