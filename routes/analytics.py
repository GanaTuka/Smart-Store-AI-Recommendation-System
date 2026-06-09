from flask import Blueprint, jsonify, render_template

from analytics.category_analysis import get_top_categories
from analytics.customer_analysis import get_top_customer_states
from analytics.payment_analysis import get_payment_breakdown
from analytics.review_analysis import get_average_review_score, get_review_distribution
from analytics.sales_analysis import get_sales_summary
from analytics.top_products import get_top_products

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/admin")
def admin_page():
    return render_template("admin.html")


@analytics_bp.route("/analytics/top-products")
def top_products_api():
    return jsonify(get_top_products())


@analytics_bp.route("/analytics/summary")
def summary_api():
    summary = get_sales_summary()
    summary["average_review_score"] = get_average_review_score()
    return jsonify(summary)


@analytics_bp.route("/analytics/top-categories")
def top_categories_api():
    return jsonify(get_top_categories())


@analytics_bp.route("/analytics/payment-breakdown")
def payment_breakdown_api():
    return jsonify(get_payment_breakdown())


@analytics_bp.route("/analytics/review-distribution")
def review_distribution_api():
    return jsonify(get_review_distribution())


@analytics_bp.route("/analytics/customer-states")
def customer_states_api():
    return jsonify(get_top_customer_states())
