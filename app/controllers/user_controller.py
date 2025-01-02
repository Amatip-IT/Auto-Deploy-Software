from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from ..database import db, handle_db_error

# Blueprint for user-related routes
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided."}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"message": "All fields are required."}), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "User with this username or email already exists."}), 409

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        handle_db_error(e)
        return jsonify({"message": "Error registering user."}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a JWT."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided."}), 400

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"message": "Both username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password."}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "message": "Login successful."}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Retrieve the profile of the authenticated user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }
    return jsonify(user_data), 200

@user_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the profile of the authenticated user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided."}), 400

    username = data.get('username')
    email = data.get('email')

    if username:
        user.username = username
    if email:
        user.email = email

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully."}), 200
    except Exception as e:
        handle_db_error(e)
        return jsonify({"message": "Error updating profile."}), 500

@user_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    """Delete the authenticated user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."}), 200
    except Exception as e:
        handle_db_error(e)
        return jsonify({"message": "Error deleting user."}), 500
