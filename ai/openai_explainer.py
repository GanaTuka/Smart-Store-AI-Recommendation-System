def explain_recommendation(product, customer_categories):
    categories = ", ".join(customer_categories[:3]) or "popular store categories"

    if product.get("model") == "popular_fallback":
        return (
            f"This product is recommended because it is one of the most purchased items "
            f"in the Olist catalog, with {product['popularity']} sales."
        )

    return (
        f"This product matches the customer's purchase profile from {categories}. "
        f"The local ML model scored it {product['score']} based on category similarity, "
        f"average price, product attributes, and popularity."
    )
