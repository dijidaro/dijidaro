import os
from flask import Flask

# Create and configure app.
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule("/", endpoint="home")
    
    return app