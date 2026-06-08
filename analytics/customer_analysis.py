from database.db import fetch_all


def get_customer_order_counts():
    return fetch_all(
        """
        SELECT u.id, u.name, COUNT(o.id) AS order_count
        FROM users u
        LEFT JOIN orders o ON o.user_id = u.id
        GROUP BY u.id, u.name
        ORDER BY order_count DESC
        """
    )
