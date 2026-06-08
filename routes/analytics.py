from flask import Blueprint, jsonify, render_template

from analytics.top_products import get_top_products

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/admin")
def admin_page():
    return render_template("admin.html")


@analytics_bp.route("/analytics/top-products")
def top_products_api():
    return jsonify(get_top_products())
