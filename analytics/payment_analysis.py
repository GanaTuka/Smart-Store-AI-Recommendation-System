from database.db import fetch_all


def get_payment_breakdown():
    return fetch_all(
        """
        SELECT
            payment_type,
            COUNT(*) AS payment_count,
            ROUND(SUM(payment_value), 2) AS payment_value
        FROM payments
        GROUP BY payment_type
        ORDER BY payment_value DESC
        """
    )
