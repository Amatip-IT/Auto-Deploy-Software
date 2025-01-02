import os
import boto3

class AWSConfig:
    """
    Configuration and utility class for managing AWS resources.
    """
    def __init__(self):
        self.access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION", "us-east-1")

        if not self.access_key_id or not self.secret_access_key:
            raise ValueError("AWS credentials are not properly configured.")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )

        self.route53_client = boto3.client(
            "route53",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )

        self.cloudfront_client = boto3.client(
            "cloudfront",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )

        self.acm_client = boto3.client(
            "acm",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )

    def validate_credentials(self):
        """
        Validate AWS credentials by making a simple API call.
        """
        try:
            self.s3_client.list_buckets()
            return True
        except Exception as e:
            raise ValueError(f"AWS credentials validation failed: {e}")

    def get_s3_client(self):
        """Return the S3 client instance."""
        return self.s3_client

    def get_route53_client(self):
        """Return the Route 53 client instance."""
        return self.route53_client

    def get_cloudfront_client(self):
        """Return the CloudFront client instance."""
        return self.cloudfront_client

    def get_acm_client(self):
        """Return the ACM client instance."""
        return self.acm_client

# Utility function to initialize AWSConfig
def init_aws_config():
    """
    Initialize and validate AWS configuration.
    
    :return: AWSConfig instance
    """
    aws_config = AWSConfig()
    aws_config.validate_credentials()
    return aws_config
