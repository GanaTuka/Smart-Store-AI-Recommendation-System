from database.db import fetch_all


def recommend_products(user_id, limit=3):
    bought_categories = fetch_all(
        """
        SELECT DISTINCT p.category
        FROM orders o
        JOIN products p ON p.id = o.product_id
        WHERE o.user_id = %s
        """,
        (user_id,),
    )
    categories = [row["category"] for row in bought_categories]

    if categories:
        placeholders = ", ".join(["%s"] * len(categories))
        query = f"""
            SELECT p.id, p.name, p.category, p.price
            FROM products p
            WHERE p.category IN ({placeholders})
              AND p.id NOT IN (SELECT product_id FROM orders WHERE user_id = %s)
            ORDER BY p.rating DESC, p.price ASC
            LIMIT %s
        """
        recommendations = fetch_all(query, (*categories, user_id, limit))
    else:
        recommendations = []

    if len(recommendations) < limit:
        fallback = fetch_all(
            """
            SELECT id, name, category, price
            FROM products
            ORDER BY rating DESC, price ASC
            LIMIT %s
            """,
            (limit - len(recommendations),),
        )
        seen = {item["id"] for item in recommendations}
        recommendations.extend(item for item in fallback if item["id"] not in seen)

    return recommendations[:limit]
