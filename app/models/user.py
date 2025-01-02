from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token

db = SQLAlchemy()

class User(db.Model):
    """User Model for storing user-related details."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the hashed password."""
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expires_in=3600):
        """Generates a JWT token for the user."""
        return create_access_token(identity={"id": self.id, "username": self.username}, expires_delta=expires_in)

    @staticmethod
    def find_by_username(username):
        """Finds a user by username."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        """Finds a user by email."""
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.username}>"
