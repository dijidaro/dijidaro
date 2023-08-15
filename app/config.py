import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    # Create and configure app.
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    csrf.init_app(app)
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule("/", endpoint="home")
    
    import auth
    app.register_blueprint(auth.bp)

    return app
