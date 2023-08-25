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

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    code = db.Column(db.String, nullable=False, unique=True)
    abbr = db.Column(db.String, nullable=False, unique=True)
    learning_area = db.Column(db.String, nullable=False)
    
    def __repr__(self) -> str:
        return f"Subject(name={self.name}, code={self.code}, abbreviation={self.abbr}, learning_area={self.learning_area})"

class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"School(name={self.name}, code={self.code}, category={self.category}, gender={self.gender})"

class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    subject = db.relationship("Subject", backref=db.backref("resources", lazy=True))
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"))
    school = db.relationship("School", backref=db.backref("resources", lazy=True))
    file_url = db.Column(db.String, nullable=False, unique=True)
    thumbnail_url = db.Column(db.String, nullable=False, unique=True)
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.String, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
