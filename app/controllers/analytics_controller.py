from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from ..services.analytics_service import AnalyticsService

# Create blueprint for analytics
analytics_bp = Blueprint('analytics', __name__)

# Initialize analytics service
analytics_service = AnalyticsService()

@analytics_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Endpoint to fetch analytics summary.

    :return: JSON response with analytics summary
    """
    try:
        summary = analytics_service.get_summary()
        return jsonify({"status": "success", "data": summary}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@analytics_bp.route('/traffic', methods=['GET'])
def get_traffic_data():
    """
    Endpoint to fetch traffic analytics data.

    :return: JSON response with traffic data
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        traffic_data = analytics_service.get_traffic_data(start_date, end_date)
        return jsonify({"status": "success", "data": traffic_data}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@analytics_bp.route('/performance', methods=['GET'])
def get_performance_metrics():
    """
    Endpoint to fetch application performance metrics.

    :return: JSON response with performance metrics
    """
    try:
        performance_data = analytics_service.get_performance_metrics()
        return jsonify({"status": "success", "data": performance_data}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@analytics_bp.route('/optimize', methods=['POST'])
def optimize_resources():
    """
    Endpoint to suggest resource optimization based on analytics.

    :return: JSON response with optimization suggestions
    """
    try:
        optimization_data = analytics_service.get_optimization_suggestions()
        return jsonify({"status": "success", "data": optimization_data}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
