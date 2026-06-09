from database.db import fetch_all


def get_top_categories(limit=8):
    return fetch_all(
        """
        SELECT
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
            COUNT(*) AS units_sold,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        GROUP BY category
        ORDER BY revenue DESC, units_sold DESC
        LIMIT %s
        """,
        (limit,),
    )
