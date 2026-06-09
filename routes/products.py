from flask import Blueprint, jsonify, render_template, request

from ai.product_search import DEFAULT_CUSTOMER_ID, search_products_with_ai
from database.db import get_products

products_bp = Blueprint("products", __name__)


@products_bp.route("/products")
def products_api():
    return jsonify(get_products())


@products_bp.route("/products/search-ai")
def products_ai_search_api():
    query = request.args.get("q", "")
    customer_id = request.args.get("customer_id", DEFAULT_CUSTOMER_ID)
    return jsonify(search_products_with_ai(query, customer_id))


@products_bp.route("/product-list")
def products_page():
    return render_template("products.html")
