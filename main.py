from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from utils.error_handler import handle_api_error, handle_db_error, handle_generic_error
from config import get_config
from models import db
from services.task_scheduler import celery_app
from app.controllers.user_controller import user_blueprint
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MainApp")

def create_app(config_name):
    """Application factory to initialize Flask app."""
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    # Register blueprints
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    # Error handling
    register_error_handlers(app)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app

def register_error_handlers(app):
    """Register custom error handlers."""
    app.register_error_handler(400, handle_api_error)
    app.register_error_handler(500, handle_generic_error)
    app.register_error_handler(Exception, handle_generic_error)

if __name__ == '__main__':
    # Select configuration environment
    config_name = 'development'  # Replace with `production` or `testing` as needed
    app = create_app(config_name)

    # Log startup message
    logger.info(f"Starting the application in {config_name} mode.")

    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])
