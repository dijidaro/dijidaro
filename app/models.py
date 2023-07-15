from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import app

db = SQLAlchemy(app)

class Students(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    gender = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

with app.app_context():
    db.create_all()
