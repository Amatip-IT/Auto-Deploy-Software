from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..services.domain_service import DomainService
from ..utils.validators import validate_domain_name

# Create Blueprint
domain_bp = Blueprint('domain', __name__)

domain_service = DomainService()

@domain_bp.route('/register', methods=['POST'])
@jwt_required()
def register_domain():
    """
    Endpoint to register a domain.

    Request Body:
    {
        "domain_name": "example.com"
    }

    :return: JSON response with registration status.
    """
    data = request.get_json()

    if not data or 'domain_name' not in data:
        return jsonify({"error": "Domain name is required."}), 400

    domain_name = data['domain_name']

    # Validate domain name
    if not validate_domain_name(domain_name):
        return jsonify({"error": "Invalid domain name."}), 400

    try:
        # Call the domain service to register the domain
        result = domain_service.register_domain(domain_name)
        return jsonify({"message": "Domain registered successfully.", "details": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@domain_bp.route('/status/<string:domain_name>', methods=['GET'])
@jwt_required()
def check_domain_status(domain_name):
    """
    Endpoint to check the status of a domain.

    :param domain_name: The domain name to check.
    :return: JSON response with domain status.
    """
    try:
        # Call the domain service to check domain status
        status = domain_service.get_domain_status(domain_name)
        return jsonify({"domain_name": domain_name, "status": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@domain_bp.route('/delete/<string:domain_name>', methods=['DELETE'])
@jwt_required()
def delete_domain(domain_name):
    """
    Endpoint to delete a domain.

    :param domain_name: The domain name to delete.
    :return: JSON response with deletion status.
    """
    try:
        # Call the domain service to delete the domain
        domain_service.delete_domain(domain_name)
        return jsonify({"message": f"Domain {domain_name} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
