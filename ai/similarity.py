from functools import lru_cache

from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from database.db import fetch_all


CATALOG_LIMIT = 5000


def _as_float(value):
    return float(value or 0)


@lru_cache(maxsize=1)
def build_product_model():
    products = fetch_all(
        """
        SELECT
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm,
            ROUND(AVG(oi.price), 2) AS avg_price,
            COUNT(oi.order_id) AS popularity
        FROM products p
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        LEFT JOIN order_items oi
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            category,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm
        HAVING popularity > 0
        ORDER BY popularity DESC
        LIMIT %s
        """,
        (CATALOG_LIMIT,),
    )

    texts = [f"{product['category']} {product['category']} product" for product in products]
    numeric_features = [
        [
            _as_float(product["avg_price"]),
            _as_float(product["popularity"]),
            _as_float(product["product_weight_g"]),
            _as_float(product["product_length_cm"]),
            _as_float(product["product_height_cm"]),
            _as_float(product["product_width_cm"]),
        ]
        for product in products
    ]

    vectorizer = TfidfVectorizer()
    text_matrix = vectorizer.fit_transform(texts)
    scaler = StandardScaler(with_mean=False)
    numeric_matrix = scaler.fit_transform(numeric_features)
    feature_matrix = hstack([text_matrix, numeric_matrix]).tocsr()

    return {
        "products": products,
        "feature_matrix": feature_matrix,
    }


def rank_similar_products(purchased_product_ids, limit=3):
    model = build_product_model()
    products = model["products"]
    feature_matrix = model["feature_matrix"]
    purchased_ids = set(purchased_product_ids)
    purchased_indexes = [
        index
        for index, product in enumerate(products)
        if product["product_id"] in purchased_ids
    ]

    if not purchased_indexes:
        return _popular_fallback(products, limit)

    customer_profile = csr_matrix(feature_matrix[purchased_indexes].mean(axis=0))
    similarities = cosine_similarity(customer_profile, feature_matrix).ravel()
    ranked_indexes = similarities.argsort()[::-1]

    recommendations = []
    for index in ranked_indexes:
        product = products[index]
        if product["product_id"] in purchased_ids:
            continue

        recommendations.append(_format_recommendation(product, similarities[index], "ml_similarity"))
        if len(recommendations) == limit:
            break

    return recommendations


def _popular_fallback(products, limit):
    return [
        _format_recommendation(product, 0.0, "popular_fallback")
        for product in products[:limit]
    ]


def _format_recommendation(product, similarity, model_type):
    return {
        "product_id": product["product_id"],
        "category": product["category"],
        "avg_price": _as_float(product["avg_price"]),
        "score": round(float(similarity), 4),
        "popularity": int(product["popularity"] or 0),
        "model": model_type,
    }
