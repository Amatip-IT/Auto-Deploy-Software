import os
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

class SecretsManager:
    """
    Handles retrieving secrets from AWS Secrets Manager or environment variables.
    """

    def __init__(self):
        self.client = boto3.client(
            "secretsmanager",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def get_secret(self, secret_name):
        """
        Retrieves a secret value from AWS Secrets Manager.

        :param secret_name: Name of the secret in AWS Secrets Manager.
        :return: The secret value as a dictionary (JSON) or string.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)

            if "SecretString" in response:
                return response["SecretString"]
            elif "SecretBinary" in response:
                return response["SecretBinary"].decode("utf-8")
        except NoCredentialsError:
            raise ValueError("AWS credentials not found.")
        except BotoCoreError as e:
            raise ValueError(f"Failed to retrieve secret {secret_name}: {e}")

    def get_env_or_secret(self, key, secret_name=None):
        """
        Retrieves a value from environment variables or AWS Secrets Manager.

        :param key: Environment variable key to check first.
        :param secret_name: AWS Secrets Manager key to fallback to.
        :return: The retrieved value.
        """
        env_value = os.getenv(key)

        if env_value:
            return env_value

        if secret_name:
            return self.get_secret(secret_name)

        raise ValueError(f"Value for {key} not found in environment variables or AWS Secrets Manager.")

# Singleton instance for shared use
secrets_manager = SecretsManager()

# Example usage (comment out in production):
# db_password = secrets_manager.get_env_or_secret("DB_PASSWORD", "my-db-secret")
