import os
from config import create_app
from models import db
from flask_migrate import Migrate
import logging

app = create_app()

migrate = Migrate(app, db)

with app.app_context():
    try:
        db.create_all()
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error(f"DB Error: {e}.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
