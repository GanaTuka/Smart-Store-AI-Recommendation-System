from database.db import fetch_all


def get_customer_order_counts(limit=10):
    return fetch_all(
        """
        SELECT
            c.customer_id,
            c.customer_city,
            c.customer_state,
            COUNT(o.order_id) AS order_count
        FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_city, c.customer_state
        ORDER BY order_count DESC
        LIMIT %s
        """,
        (limit,),
    )
