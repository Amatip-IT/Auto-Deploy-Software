from flask import Blueprint

# Import all individual blueprints from controllers
from .auth_controller import auth_bp
from .deploy_controller import deploy_bp
from .domain_controller import domain_bp
from .analytics_controller import analytics_bp
from .ai_controller import ai_bp

__all__ = [
    "auth_bp",
    "deploy_bp",
    "domain_bp",
    "analytics_bp",
    "ai_bp",
]

def register_blueprints(app):
    """
    Registers all blueprints to the Flask application instance.

    :param app: Flask application instance
    """
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(deploy_bp, url_prefix="/api/deploy")
    app.register_blueprint(domain_bp, url_prefix="/api/domain")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
