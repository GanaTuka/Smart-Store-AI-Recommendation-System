from database.db import fetch_all


def get_top_products(limit=5):
    return fetch_all(
        """
        SELECT
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
            COUNT(*) AS units_sold,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        GROUP BY p.product_id, category
        ORDER BY units_sold DESC, revenue DESC
        LIMIT %s
        """,
        (limit,),
    )
