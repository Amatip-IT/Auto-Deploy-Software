from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import openai
import logging

# Initialize Blueprint
ai_bp = Blueprint('ai', __name__)

# Logger setup
logger = logging.getLogger(__name__)

# AI Assistant Endpoint
@ai_bp.route('/recommend', methods=['POST'])
@jwt_required()
def ai_recommendations():
    """
    Provides AI-powered recommendations based on user input.

    Expects JSON payload:
    {
        "input": "User input text",
        "context": "Optional context for better recommendations"
    }

    :return: JSON response with AI-generated recommendations.
    """
    try:
        data = request.get_json()
        user_input = data.get('input')
        context = data.get('context', '')

        if not user_input:
            return jsonify({"error": "Input is required."}), 400

        # Call OpenAI API
        openai.api_key = current_app.config.get("OPENAI_API_KEY")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Provide recommendations based on: {user_input}. Context: {context}",
            max_tokens=150
        )

        ai_output = response.choices[0].text.strip()

        return jsonify({"recommendations": ai_output}), 200

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return jsonify({"error": "Failed to generate recommendations. Please try again later."}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

# AI Health Check Endpoint
@ai_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for AI service.

    :return: JSON response indicating the AI service status.
    """
    return jsonify({"status": "AI service is operational."}), 200
