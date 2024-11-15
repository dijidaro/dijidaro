import os
from flask import Flask

def create_app():
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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