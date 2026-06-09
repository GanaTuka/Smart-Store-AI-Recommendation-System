import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()


def explain_recommendation(product, customer_categories):
    fallback = build_fallback_explanation(product, customer_categories)

    if os.getenv("OLLAMA_ENABLED", "true").lower() != "true":
        product["explanation_source"] = "template_fallback"
        return fallback

    prompt = build_prompt(product, customer_categories, fallback)
    explanation = call_ollama(prompt)
    if explanation and is_safe_explanation(explanation):
        product["explanation_source"] = f"ollama:{os.getenv('OLLAMA_MODEL', 'gemma3:1b')}"
        return explanation

    product["explanation_source"] = "template_fallback"
    return fallback


def build_prompt(product, customer_categories, base_explanation):
    categories = ", ".join(customer_categories[:5]) or "unknown previous categories"
    mode = "popular fallback" if product.get("model") == "popular_fallback" else "content-based similarity"
    return f"""
You are an AI assistant for a smart e-commerce store.
Rewrite the base reason into one friendly sentence under 25 words.
Do not add any new product details.
Do not invent product names, item types, brands, materials, smells, colors, features, or benefits.
Do not use emojis.
Keep the meaning of the base reason.

Customer purchase categories: {categories}
Recommended product category: {product['category']}
Average price: ${product['avg_price']:.2f}
Store popularity: {product['popularity']} sales
Recommendation similarity score: {product['score']}
Recommendation method: {mode}
Base reason: {base_explanation}
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
            "temperature": 0.0,
            "num_predict": 60,
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


def is_safe_explanation(explanation):
    text = explanation.lower()
    starts_like_reason = text.startswith("recommended") or text.startswith("this product is recommended")
    invented_detail_words = [
        "chair",
        "desk",
        "towel",
        "blanket",
        "wood",
        "wooden",
        "metal",
        "plush",
        "aromatherapy",
        "scent",
        "color",
        "sturdy",
        "rectangular",
    ]
    has_invented_details = any(word in text for word in invented_detail_words)
    return starts_like_reason and not has_invented_details


def build_fallback_explanation(product, customer_categories):
    categories = ", ".join(customer_categories[:3]) or "popular store categories"

    if product.get("model") == "popular_fallback":
        return (
            f"Recommended because this customer has no usable purchase-history match yet, "
            f"so we selected a popular {product['category']} item with {product['popularity']} sales."
        )

    return (
        f"Recommended because it matches this customer's history in {categories}. "
        f"The content-based AI model gave it a similarity score of {product['score']}."
    )
