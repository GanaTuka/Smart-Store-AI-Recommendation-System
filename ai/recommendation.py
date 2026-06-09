from ai.openai_explainer import explain_recommendation
from ai.similarity import rank_similar_products
from database.db import fetch_all


def recommend_products(customer_id, limit=3):
    history = fetch_all(
        """
        SELECT DISTINCT
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        WHERE o.customer_id = %s
          AND p.product_id IS NOT NULL
        """,
        (customer_id,),
    )
    purchased_product_ids = [row["product_id"] for row in history]
    customer_categories = list(dict.fromkeys(row["category"] for row in history))

    recommendations = rank_similar_products(purchased_product_ids, limit)
    for product in recommendations:
        product["explanation"] = explain_recommendation(product, customer_categories)

    return recommendations
