from flask import Blueprint, jsonify, render_template

from ai.recommendation import recommend_products

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations")
def recommendations_page():
    return render_template("recommendations.html")


@recommendations_bp.route("/recommendations/<int:user_id>")
def recommendations_api(user_id):
    return jsonify(recommend_products(user_id))
