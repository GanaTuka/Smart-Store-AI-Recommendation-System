from flask import Flask, render_template
from routes.analytics import analytics_bp
from routes.auth import auth_bp
from routes.products import products_bp
from routes.recommendations import recommendations_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hackathon-secret-key"

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(analytics_bp)

    @app.route("/")
    def home():
        return render_template("dashboard.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
