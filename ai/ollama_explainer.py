import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()


def explain_recommendation(product, customer_categories):
    fallback = build_fallback_explanation(product, customer_categories)

    if os.getenv("OLLAMA_ENABLED", "true").lower() != "true":
        return fallback

    prompt = build_prompt(product, customer_categories)
    explanation = call_ollama(prompt)
    return explanation or fallback


def build_prompt(product, customer_categories):
    categories = ", ".join(customer_categories[:5]) or "unknown previous categories"
    return f"""
You are an AI assistant for a smart e-commerce store.
Write one short, friendly, personalized recommendation reason.
Do not mention internal IDs unless necessary.
Keep it under 35 words.

Customer purchase categories: {categories}
Recommended product category: {product['category']}
Average price: ${product['avg_price']:.2f}
Store popularity: {product['popularity']} sales
Recommendation similarity score: {product['score']}
""".strip()


def call_ollama(prompt):
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    timeout = float(os.getenv("OLLAMA_TIMEOUT", "8"))
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.4,
            "num_predict": 80,
        },
    }
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, json.JSONDecodeError):
        return None

    explanation = data.get("response", "").strip()
    return explanation if explanation else None


def build_fallback_explanation(product, customer_categories):
    categories = ", ".join(customer_categories[:3]) or "popular store categories"

    if product.get("model") == "popular_fallback":
        return (
            f"Recommended because it is a popular Olist item with "
            f"{product['popularity']} sales and an average price of ${product['avg_price']:.2f}."
        )

    return (
        f"Recommended because it matches this customer's history in {categories}. "
        f"The content-based AI model gave it a similarity score of {product['score']}."
    )
