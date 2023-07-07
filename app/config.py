from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule("/", endpoint="home")
    
    return app