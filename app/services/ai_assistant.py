import openai
import logging
import os

class AIAssistant:
    """
    AI Assistant Service to provide NLP-based guidance and recommendations
    for deployment settings, resource optimization, and user support.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OpenAI API Key is not set in environment variables.")
        openai.api_key = self.api_key

    def generate_response(self, prompt, max_tokens=150, temperature=0.7):
        """
        Generate AI response based on a user prompt using OpenAI's API.

        Args:
            prompt (str): The input prompt for the AI assistant.
            max_tokens (int): Maximum number of tokens in the response.
            temperature (float): Creativity level for the response.

        Returns:
            str: Generated response from the AI model.
        """
        try:
            logging.info("Generating AI response...")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Error generating AI response: {e}")
            return "I'm sorry, I couldn't process your request. Please try again later."

    def recommend_resources(self, app_type, traffic_estimate):
        """
        Recommend resources based on application type and expected traffic.

        Args:
            app_type (str): Type of application (e.g., eCommerce, blog, SaaS).
            traffic_estimate (str): Expected traffic (e.g., low, medium, high).

        Returns:
            str: AI-generated recommendation for resource allocation.
        """
        prompt = (
            f"I am deploying a {app_type} application with {traffic_estimate} traffic. "
            "Recommend an optimal AWS resource configuration including EC2 instance types, "
            "RDS database specs, and S3 bucket settings."
        )
        return self.generate_response(prompt)

    def guide_deployment_steps(self, framework, hosting_environment):
        """
        Provide step-by-step guidance for deploying an application.

        Args:
            framework (str): Development framework (e.g., React, Django).
            hosting_environment (str): Hosting environment (e.g., AWS, on-premise).

        Returns:
            str: AI-generated deployment steps.
        """
        prompt = (
            f"Guide me through the steps to deploy a {framework} application on {hosting_environment}. "
            "Include best practices for scalability and security."
        )
        return self.generate_response(prompt)

    def debug_issues(self, error_message):
        """
        Offer troubleshooting tips for a given error message.

        Args:
            error_message (str): The error message or issue description.

        Returns:
            str: AI-generated troubleshooting advice.
        """
        prompt = (
            f"I encountered this error during deployment: '{error_message}'. "
            "What steps should I take to resolve this issue?"
        )
        return self.generate_response(prompt)

    def optimize_costs(self, current_config):
        """
        Suggest cost-saving measures based on current resource configuration.

        Args:
            current_config (str): Description of the current resource setup.

        Returns:
            str: AI-generated cost optimization suggestions.
        """
        prompt = (
            f"My current AWS configuration is: {current_config}. "
            "Suggest ways to reduce costs without compromising performance."
        )
        return self.generate_response(prompt)

    def assist_with_documentation(self, topic):
        """
        Generate documentation or explain concepts related to deployment.

        Args:
            topic (str): The topic for which documentation or explanation is needed.

        Returns:
            str: AI-generated documentation or explanation.
        """
        prompt = f"Write detailed documentation or explain the following topic: {topic}."
        return self.generate_response(prompt)


# Example Usage (for testing purposes)
if __name__ == "__main__":
    assistant = AIAssistant()

    # Example 1: Recommend Resources
    print(assistant.recommend_resources("eCommerce", "high"))

    # Example 2: Deployment Steps
    print(assistant.guide_deployment_steps("React", "AWS"))

    # Example 3: Debugging Advice
    print(assistant.debug_issues("Error: Cannot connect to database."))

    # Example 4: Cost Optimization
    print(assistant.optimize_costs("2 t2.micro EC2 instances, 1 RDS db.t3.micro database."))

    # Example 5: Documentation Assistance
    print(assistant.assist_with_documentation("CI/CD pipelines for Python applications."))
