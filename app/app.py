import os
from config import create_app
# from models import db
# from flask_migrate import Migrate

app = create_app()

# bootstrap database migrate commands
# db.init_app(app)
# migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

