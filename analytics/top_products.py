from database.db import fetch_all


def get_top_products(limit=5):
    return fetch_all(
        """
        SELECT p.id, p.name, SUM(o.quantity) AS units_sold
        FROM orders o
        JOIN products p ON p.id = o.product_id
        GROUP BY p.id, p.name
        ORDER BY units_sold DESC
        LIMIT %s
        """,
        (limit,),
    )
