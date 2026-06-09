from database.db import fetch_all


def get_review_distribution():
    return fetch_all(
        """
        SELECT
            review_score,
            COUNT(*) AS review_count
        FROM reviews
        WHERE review_score IS NOT NULL
        GROUP BY review_score
        ORDER BY review_score
        """
    )


def get_average_review_score():
    rows = fetch_all(
        """
        SELECT ROUND(AVG(review_score), 2) AS average_review_score
        FROM reviews
        WHERE review_score IS NOT NULL
        """
    )
    return rows[0]["average_review_score"] if rows else 0
