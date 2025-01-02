from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from ..models.user import User
from ..database import db

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Register Route
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint for user registration.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists."}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create and save the user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully."}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        # Find user in the database
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid username or password."}), 401

        # Create access token
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "message": "Login successful."}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Get Current User Route
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Endpoint to get current user details.
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found."}), 404

        return jsonify({"id": user.id, "username": user.username}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
