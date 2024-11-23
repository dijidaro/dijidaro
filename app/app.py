import os
from app import create_app
from app.models import db
from flask_migrate import Migrate

app = create_app()

# Initialize database
db.init_app(app)

# Set up Flask-Migrate for databas migrations
migrate = Migrate(app, db)

if app.config.get("ENV") == "development":
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
