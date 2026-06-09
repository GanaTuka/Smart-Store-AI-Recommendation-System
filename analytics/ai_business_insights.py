from ai.ollama_explainer import call_ollama
from analytics.category_analysis import get_top_categories
from analytics.payment_analysis import get_payment_breakdown
from analytics.review_analysis import get_average_review_score
from analytics.sales_analysis import get_sales_summary
from analytics.top_products import get_top_products


def get_business_recommendation():
    summary = get_sales_summary()
    categories = get_top_categories(3)
    products = get_top_products(3)
    payments = get_payment_breakdown()
    average_review = get_average_review_score()

    top_category = categories[0] if categories else {"category": "unknown", "revenue": 0, "units_sold": 0}
    top_product = products[0] if products else {"category": "unknown", "units_sold": 0, "revenue": 0}
    top_payment = payments[0] if payments else {"payment_type": "unknown", "payment_value": 0}

    fallback = (
        f"Focus future promotions on {top_category['category']} because it leads revenue "
        f"with ${float(top_category['revenue'] or 0):,.0f} and {top_category['units_sold']} units sold. "
        f"Keep top products in stock, especially {top_product['category']} items, and monitor reviews "
        f"because the current average score is {average_review}/5."
    )

    prompt = f"""
You are a business analyst for an e-commerce admin dashboard.
Write one practical recommendation for the store owner in 2 short sentences.
Use only the numbers below. Do not invent details.

Total revenue: ${float(summary.get('total_sales') or 0):,.0f}
Total orders: {summary.get('total_orders')}
Top category: {top_category['category']} with ${float(top_category['revenue'] or 0):,.0f} revenue and {top_category['units_sold']} units sold
Top product category: {top_product['category']} with {top_product['units_sold']} units sold
Top payment method: {top_payment['payment_type']}
Average review score: {average_review}/5

Base recommendation: {fallback}
""".strip()
    llm_text = call_ollama(prompt)

    return {
        "recommendation": llm_text or fallback,
        "source": "ollama" if llm_text else "template_fallback",
        "top_category": top_category,
        "top_product": top_product,
        "average_review_score": average_review,
    }
