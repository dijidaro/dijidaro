from flask import Flask
from .config import config_by_name
from flask_wtf.csrf import CSRFProtect
import os

csrf = CSRFProtect()

# Configuration mapping
config_by_name = {
    'development': 'app.config.DevelopmentConfig',
    'production': 'app.config.ProductionConfig',
    'testing': 'app.config.TestingConfig',
}

def create_app(config_name=None):
    """Create and configure the Flask app instance."""
    app = Flask(__name__, instance_relative_config=True)

    csrf.init_app(app)

    # Configure Logging
    from .logging_config import configure_logging
    configure_logging(app)

    config_name = config_name or os.getenv("FLASK_ENV", "development")

    # Load configuration from the config class
    app.config.from_object(config_by_name[config_name])

    from .error_handlers import init_error_handlers
    init_error_handlers(app)

    from .routes.home import home_bp
    app.register_blueprint(home_bp)
    app.add_url_rule("/", endpoint="home")

    from .routes.explore import explore_bp
    app.register_blueprint(explore_bp)

    from .routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
    