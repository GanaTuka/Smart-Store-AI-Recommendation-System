import re

from ai.ollama_explainer import call_ollama
from database.db import fetch_all


DEFAULT_CUSTOMER_ID = "06b8999e2fba1a1fbc88172c00ba8bc7"


def search_products_with_ai(query, customer_id=DEFAULT_CUSTOMER_ID, limit=9):
    query = (query or "").strip()
    max_price = extract_budget(query)
    terms = extract_terms(query)
    customer_categories = get_customer_categories(customer_id)
    products = search_products(terms, max_price, limit)

    if not products and customer_categories:
        products = search_products(customer_categories[:2], max_price, limit)

    if not products:
        products = get_popular_products(limit)

    answer = explain_search(query, products, customer_categories, max_price)
    return {
        "query": query,
        "customer_id": customer_id,
        "max_price": max_price,
        "customer_categories": customer_categories,
        "answer": answer,
        "products": products,
    }


def extract_budget(query):
    match = re.search(r"(?:\$\s*)?(\d+(?:\.\d+)?)\s*(?:\$|usd|dollars)?", query.lower())
    return float(match.group(1)) if match else None


def extract_terms(query):
    ignored = {
        "worth",
        "under",
        "below",
        "less",
        "than",
        "cheap",
        "best",
        "top",
        "pick",
        "picks",
        "product",
        "products",
        "for",
        "of",
        "the",
        "and",
    }
    words = re.findall(r"[a-zA-Z_]+", query.lower().replace("garden tool", "garden_tools"))
    return [word for word in words if word not in ignored and len(word) > 2]


def get_customer_categories(customer_id):
    rows = fetch_all(
        """
        SELECT
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
            COUNT(*) AS purchases
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        WHERE o.customer_id = %s
        GROUP BY category
        ORDER BY purchases DESC
        LIMIT 5
        """,
        (customer_id,),
    )
    return [row["category"] for row in rows]


def search_products(terms, max_price, limit):
    where = []
    params = []

    if terms:
        category_conditions = []
        for term in terms:
            category_conditions.append("COALESCE(t.product_category_name_english, p.product_category_name, '') LIKE %s")
            params.append(f"%{term}%")
        where.append(f"({' OR '.join(category_conditions)})")

    having = ""
    if max_price is not None:
        having = "HAVING avg_price <= %s"
        params.append(max_price)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    params.append(limit)

    return fetch_all(
        f"""
        SELECT
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
            ROUND(AVG(oi.price), 2) AS avg_price,
            COUNT(*) AS popularity
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        LEFT JOIN category_translation t
            ON t.product_category_name = p.product_category_name
        {where_sql}
        GROUP BY p.product_id, category
        {having}
        ORDER BY popularity DESC, avg_price ASC
        LIMIT %s
        """,
        tuple(params),
    )


def get_popular_products(limit):
    return search_products([], None, limit)


def explain_search(query, products, customer_categories, max_price):
    top = products[0]
    category_history = ", ".join(customer_categories[:3]) or "no previous category history"
    budget_text = f" under ${max_price:.2f}" if max_price is not None else ""
    base = (
        f"Based on the database, the best match for '{query or 'popular products'}' is a "
        f"{top['category']} product{budget_text}. It averages ${float(top['avg_price']):.2f}, "
        f"has {top['popularity']} sales, and customer history includes {category_history}."
    )
    prompt = f"""
Rewrite this database-grounded shopping answer in one friendly sentence under 35 words.
Do not invent product names, brands, materials, colors, or features.
Keep the category, price, sales count, or customer-history reason.
Do not say price ranges unless the base answer says a range.
Base answer: {base}
""".strip()
    llm_answer = call_ollama(prompt)
    return llm_answer if llm_answer and is_safe_search_answer(llm_answer) else base


def is_safe_search_answer(answer):
    text = answer.lower()
    unsafe_phrases = [
        "priced between",
        "between $",
        "luxury",
        "premium material",
        "wooden",
        "metal",
        "plush",
        "aromatherapy",
        "recent purchases",
        "recent",
        "office settings",
        "featuring",
        "$500+",
        "+ furniture",
    ]
    return not any(phrase in text for phrase in unsafe_phrases)
