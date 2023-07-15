import os
from flask import Flask

# Create and configure app.
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule("/", endpoint="home")
    
    return app
