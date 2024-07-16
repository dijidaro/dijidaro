import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from errors import register_error_handlers
from models import db

csrf = CSRFProtect()

# Setup testing.
class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    UPLOAD_FOLDER = '/tmp/uploads'

def create_app(config_class=None):
    # Create and configure app.
    app = Flask(__name__, instance_relative_config=True)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_mapping({
            # Set configuration variables.
            "SECRET_KEY" : os.environ.get("SECRET_KEY"),
            "SQLALCHEMY_DATABASE_URI" : os.environ.get("DATABASE_URL").replace("://", "ql://", 1),
            "SQLALCHEMY_TRACK_MODIFICATIONS" : False,
            "TESSDATA_PREFIX" : os.environ.get("TESSDATA_PREFIX"),
            "UPLOAD_FOLDER" : os.path.join(os.path.dirname(__file__), "uploads")
        })
    
    app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Initialize database.
    db.init_app(app)

    # Set up CSRF protection.
    csrf.init_app(app)

    # Register error handlers.
    register_error_handlers(app)

    # Register blueprints.
    import about
    app.register_blueprint(about.bp)

    import explore
    app.register_blueprint(explore.bp)
    
    import upload
    app.register_blueprint(upload.bp)
    
    import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule("/", endpoint="index")

    import admin
    app.register_blueprint(admin.bp)
    
    import auth
    app.register_blueprint(auth.bp)

    return app
