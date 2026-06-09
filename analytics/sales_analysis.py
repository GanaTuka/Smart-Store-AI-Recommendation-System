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
    summary = rows[0] if rows else {"total_orders": 0, "total_items": 0, "total_sales": 0}
    counts = fetch_all(
        """
        SELECT
            (SELECT COUNT(*) FROM customers) AS total_customers,
            (SELECT COUNT(*) FROM products) AS total_products
        """
    )
    summary.update(counts[0] if counts else {"total_customers": 0, "total_products": 0})
    return summary
