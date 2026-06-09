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
    match_type = "exact_search"

    if not products and customer_categories:
        products = search_products(customer_categories[:2], max_price, limit)
        match_type = "customer_history"

    if not products:
        products = get_popular_products(limit)
        match_type = "popular_fallback"

    answer = explain_search(query, products, customer_categories, max_price, terms, match_type)
    return {
        "query": query,
        "customer_id": customer_id,
        "max_price": max_price,
        "customer_categories": customer_categories,
        "match_type": match_type,
        "answer": answer,
        "products": products,
    }


def extract_budget(query):
    matches = re.findall(r"(?:\$\s*)?(\d+(?:\.\d+)?)\s*(?:\$|usd|dollars)?", query.lower())
    return max(float(match) for match in matches) if matches else None


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


def explain_search(query, products, customer_categories, max_price, terms, match_type):
    top = products[0]
    category_history = ", ".join(format_category(category) for category in customer_categories[:3])
    budget_text = f" under ${max_price:.2f}" if max_price is not None else ""
    category = format_category(top["category"])

    if match_type == "customer_history":
        base = (
            f"I could not find a strong direct match for '{query}', so I looked at your shopping history. "
            f"Since you previously bought from {category_history}, I would recommend {category} products{budget_text}."
        )
    elif match_type == "popular_fallback":
        base = (
            f"I could not find enough products that clearly match '{query}'. "
            f"There is not much to show for that request, so I would start with the most popular store picks instead."
        )
    elif has_history_overlap(terms, customer_categories):
        base = (
            f"You bought similar items before in {category_history}, so I would recommend {category} products{budget_text}. "
            f"The top pick is affordable at about ${float(top['avg_price']):.2f} and has been bought {top['popularity']} times."
        )
    else:
        base = (
            f"For '{query or 'your search'}', I found {category} products{budget_text}. "
            f"You have not bought this category before, so I would choose the top store pick: about ${float(top['avg_price']):.2f} with {top['popularity']} purchases."
        )

    prompt = f"""
Rewrite this shopping answer like a helpful human store assistant.
Return only the final sentence.
Do not include options, markdown, quotes, or commentary.
Do not invent product names, brands, materials, colors, features, or price ranges.
Keep the same meaning and keep it under 45 words.
Base answer: {base}
""".strip()
    llm_answer = call_ollama(prompt)
    return llm_answer if llm_answer and is_safe_search_answer(llm_answer) else base


def format_category(category):
    return category.replace("_", " ")


def has_history_overlap(terms, customer_categories):
    if not terms:
        return False
    normalized_history = " ".join(customer_categories).lower().replace("_", " ")
    return any(term.replace("_", " ") in normalized_history for term in terms)


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
        "okay",
        "option",
        "**",
        "here are",
        "here’s",
        "here's",
        "\n",
        "stylish",
        "home décor",
        "home decor",
        "price range",
        "buyers",
        "satisfied",
        "enjoyed",
        "boasts",
        "boasting",
    ]
    return not any(phrase in text for phrase in unsafe_phrases)
