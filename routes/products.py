from flask import Blueprint, jsonify, render_template

from database.db import get_products

products_bp = Blueprint("products", __name__)


@products_bp.route("/products")
def products_api():
    return jsonify(get_products())


@products_bp.route("/product-list")
def products_page():
    return render_template("products.html")
