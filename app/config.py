# import os

# class Config:
#     """Base configuration class."""
#     SECRET_KEY = os.environ.get("SECRET_KEY")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     WTF_CSRF_ENABLED = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://postgres:jagoro1991@localhost:5432/postgres"

# class DevelopmentConfig(Config):
#     """Configuration for testing environment."""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "postgresql://postgres:password@localhost:5432/test_db"
#     PRESERVE_CONTEXT_ON_EXCEPTION = False  # Prevents tests from failing due to broken contexts
#     ENV = 'development'

# class ProductionConfig(Config):
#     """Configuration for production environment."""
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
#     ENV = 'production'

# class TestingConfig(Config):
#     """Configuration for testing environment."""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "postgresql://postgres:password@localhost:5432/test_db"
#     PRESERVE_CONTEXT_ON_EXCEPTION = False  # Prevents tests from failing due to broken contexts
#     ENV = 'testing'

# config_by_name = {
#     "development": DevelopmentConfig,
#     "produdtion": ProductionConfig,
#     "testing": TestingConfig,
# }

# # Default config
# DEFAULT_CONFIG = DevelopmentConfig

import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from error_handlers import init_error_handlers
from logging_config import configure_logging

csrf=CSRFProtect()

def create_app():
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    csrf.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "postgresql://postgres:jagoro1991@localhost:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure Logging
    configure_logging(app)
    
    # Initializee Error Handlers
    init_error_handlers(app)
    
    from routes.home import home_bp
    app.register_blueprint(home_bp)
    app.add_url_rule("/", endpoint="home")

    from routes.explore import explore_bp
    app.register_blueprint(explore_bp)

    from routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app