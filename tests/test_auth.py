import pytest
from flask import session
from app import create_app
from app.models import db, User

@pytest.fixture
def app():
    app = create_app()
    app.config.from_mapping(
        {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with app.app_context():
        db.create_all() # Create table for test database 
        yield app 
        db.session.remove()
        db.drop_all() # Clean up after test


@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user_success(client):
    # Simulate a registration POST request
    response = client.post(
        "/auth/registration",
        data={
            "first_name": "Test",
            "last_name": "User",
            "gender": "Male",
            "birth_date": "2000-01-01",
            "user_type": "Student",
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "Test@1234",
            "password2": "Test@1234",
        },
        follow_redirects=True,
    )

    # Assertions
    assert response.status_code == 200  # Ensure request was successful
    assert b"Registration successful!" in response.data  # Flash message
    user = User.query.filter_by(username="testuser").first()
    assert user is not None  # Ensure user was created in the database
    assert user.email == "testuser@example.com"

# def test_register_user_invalid_password(client):
#     response = client.post(
#         "/auth/registration",
#         data={
#             "first_name": "Test",
#             "last_name": "User",
#             "gender": "Male",
#             "birth_date": "2000-01-01",
#             "user_type": "Student",
#             "email": "testuser@example.com",
#             "username": "testuser",
#             "password": "short",
#             "password2": "short",
#         },
#         follow_redirects=True,
#     )

#     # Assertions
#     assert response.status_code == 200
#     assert b"Password must be at least 8 characters long" in response.data
#     user = User.query.filter_by(username="testuser").first()
#     assert user is None  # Ensure user was not created

# def test_register_user_duplicate_email(client):
#     # Pre-add a user to simulate duplicate registration
#     user = User(
#         first_name="Existing",
#         last_name="User",
#         gender="Male",
#         birth_date="1995-01-01",
#         user_type="Student",
#         email="testuser@example.com",
#         username="existinguser",
#         password="password",
#     )
#     db.session.add(user)
#     db.session.commit()

#     response = client.post(
#         "/auth/registration",
#         data={
#             "first_name": "Test",
#             "last_name": "User",
#             "gender": "Male",
#             "birth_date": "2000-01-01",
#             "user_type": "Student",
#             "email": "testuser@example.com",
#             "username": "testuser",
#             "password": "Test@1234",
#             "password2": "Test@1234",
#         },
#         follow_redirects=True,
#     )

#     # Assertions
#     assert response.status_code == 200
#     assert b"already existing username and/or email" in response.data
#     user = User.query.filter_by(username="testuser").first()
#     assert user is None  # Ensure duplicate user was not created