from database.db import fetch_all


def recommend_products(customer_id, limit=3):
    purchased_categories = fetch_all(
        """
        SELECT DISTINCT p.product_category_name
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE o.customer_id = %s
          AND p.product_category_name IS NOT NULL
        """,
        (customer_id,),
    )
    categories = [row["product_category_name"] for row in purchased_categories]

    if categories:
        placeholders = ", ".join(["%s"] * len(categories))
        recommendations = fetch_all(
            f"""
            SELECT
                p.product_id,
                COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
                ROUND(AVG(oi.price), 2) AS avg_price,
                COUNT(*) AS score
            FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            LEFT JOIN category_translation t
                ON t.product_category_name = p.product_category_name
            WHERE p.product_category_name IN ({placeholders})
              AND p.product_id NOT IN (
                  SELECT oi2.product_id
                  FROM orders o2
                  JOIN order_items oi2 ON oi2.order_id = o2.order_id
                  WHERE o2.customer_id = %s
              )
            GROUP BY p.product_id, category
            ORDER BY score DESC, avg_price DESC
            LIMIT %s
            """,
            (*categories, customer_id, limit),
        )
    else:
        recommendations = []

    if len(recommendations) < limit:
        fallback = fetch_all(
            """
            SELECT
                p.product_id,
                COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
                ROUND(AVG(oi.price), 2) AS avg_price,
                COUNT(*) AS score
            FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            LEFT JOIN category_translation t
                ON t.product_category_name = p.product_category_name
            GROUP BY p.product_id, category
            ORDER BY score DESC, avg_price DESC
            LIMIT %s
            """,
            (limit - len(recommendations),),
        )
        seen = {item["product_id"] for item in recommendations}
        recommendations.extend(item for item in fallback if item["product_id"] not in seen)

    return recommendations[:limit]
