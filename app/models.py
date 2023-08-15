from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    gender = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    status = db.Column(db.String, nullable=False, default="Active")

    def __repr__(self) -> str:
        return f"User(username={self.username}, gender={self.gender}, birth_date={self.birth_date})"
