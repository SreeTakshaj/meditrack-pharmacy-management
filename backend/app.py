from flask import Flask, jsonify
from flask_cors import CORS
from datetime import timedelta

from config import Config
from extensions import db, jwt, migrate # Import from extensions now

# ADD THESE IMPORTS:
from models.user import User
from models.category import Category
from models.supplier import Supplier
from models.medicine import Medicine

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS
    )

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize the extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register the Blueprints
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

   # ADD THESE NEW LINES:
    from routes.medicine_routes import medicine_bp
    app.register_blueprint(medicine_bp, url_prefix='/api/medicines')

    # Make sure these 2 lines are here!
    from routes.order_routes import order_bp
    app.register_blueprint(order_bp, url_prefix='/api/orders')

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        try:
            db.session.execute(db.text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

        return jsonify({
            "status": "ok",
            "service": "MediTrack Backend",
            "version": "1.0.0",
            "database": db_status
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=Config.APP_HOST,
        port=Config.APP_PORT,
        debug=Config.DEBUG
    )