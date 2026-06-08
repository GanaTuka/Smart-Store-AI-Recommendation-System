def simple_category_score(product, purchased_categories):
    return 1 if product.get("category") in purchased_categories else 0
