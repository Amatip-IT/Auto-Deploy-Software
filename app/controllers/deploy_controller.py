from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from ..services.deployment_service import DeploymentService
from ..utils.validators import validate_deployment_data
from ..database import db, handle_db_error

# Create Blueprint
deploy_bp = Blueprint('deploy', __name__)

# Deployment Service Instance
deployment_service = DeploymentService()

@deploy_bp.route('/create', methods=['POST'])
@jwt_required()
def create_deployment():
    """
    Endpoint to create a new deployment.

    Expects a JSON payload with deployment details.
    """
    try:
        # Parse and validate input
        data = request.get_json()
        validation_errors = validate_deployment_data(data)
        if validation_errors:
            return jsonify({"errors": validation_errors}), 400

        # Create deployment
        deployment = deployment_service.create_deployment(data)

        # Commit to the database
        db.session.add(deployment)
        db.session.commit()

        return jsonify({"message": "Deployment created successfully", "deployment": deployment.to_dict()}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        handle_db_error(e)
        return jsonify({"error": "Failed to create deployment"}), 500

@deploy_bp.route('/<int:deployment_id>', methods=['GET'])
@jwt_required()
def get_deployment(deployment_id):
    """
    Endpoint to retrieve a deployment by ID.
    """
    try:
        deployment = deployment_service.get_deployment_by_id(deployment_id)
        if not deployment:
            return jsonify({"error": "Deployment not found"}), 404

        return jsonify(deployment.to_dict()), 200

    except SQLAlchemyError as e:
        handle_db_error(e)
        return jsonify({"error": "Failed to fetch deployment"}), 500

@deploy_bp.route('/<int:deployment_id>', methods=['DELETE'])
@jwt_required()
def delete_deployment(deployment_id):
    """
    Endpoint to delete a deployment by ID.
    """
    try:
        success = deployment_service.delete_deployment(deployment_id)
        if not success:
            return jsonify({"error": "Deployment not found or could not be deleted"}), 404

        db.session.commit()
        return jsonify({"message": "Deployment deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        handle_db_error(e)
        return jsonify({"error": "Failed to delete deployment"}), 500

@deploy_bp.route('/list', methods=['GET'])
@jwt_required()
def list_deployments():
    """
    Endpoint to list all deployments.
    """
    try:
        deployments = deployment_service.list_deployments()
        return jsonify([deployment.to_dict() for deployment in deployments]), 200

    except SQLAlchemyError as e:
        handle_db_error(e)
        return jsonify({"error": "Failed to fetch deployments"}), 500
