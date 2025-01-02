import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from flask import current_app
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AWSService:
    """Service class for interacting with AWS."""

    def __init__(self):
        """Initialize AWS clients using credentials from environment variables."""
        try:
            self.s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'])
            self.route53 = boto3.client('route53', region_name=current_app.config['AWS_REGION'])
            self.acm = boto3.client('acm', region_name=current_app.config['AWS_REGION'])
            self.cloudfront = boto3.client('cloudfront', region_name=current_app.config['AWS_REGION'])
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"Error initializing AWS clients: {e}")
            raise RuntimeError("AWS credentials are missing or incomplete.")

    # S3 Bucket Operations
    def create_bucket(self, bucket_name):
        """Creates an S3 bucket."""
        try:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': current_app.config['AWS_REGION']}
            )
            logger.info(f"S3 bucket '{bucket_name}' created successfully.")
        except ClientError as e:
            logger.error(f"Failed to create S3 bucket '{bucket_name}': {e}")
            raise

    def upload_file_to_s3(self, file_path, bucket_name, key):
        """Uploads a file to an S3 bucket."""
        try:
            self.s3.upload_file(file_path, bucket_name, key)
            logger.info(f"File '{file_path}' uploaded to bucket '{bucket_name}' with key '{key}'.")
        except ClientError as e:
            logger.error(f"Failed to upload file '{file_path}' to S3: {e}")
            raise

    def generate_s3_presigned_url(self, bucket_name, key, expiration=3600):
        """Generates a presigned URL for accessing an S3 object."""
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            logger.info(f"Presigned URL generated for key '{key}' in bucket '{bucket_name}'.")
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise

    # Route 53 Domain Management
    def create_hosted_zone(self, domain_name):
        """Creates a hosted zone in Route 53."""
        try:
            response = self.route53.create_hosted_zone(
                Name=domain_name,
                CallerReference=str(hash(domain_name))
            )
            logger.info(f"Hosted zone for '{domain_name}' created successfully.")
            return response
        except ClientError as e:
            logger.error(f"Failed to create hosted zone for '{domain_name}': {e}")
            raise

    def create_dns_record(self, zone_id, record_name, record_type, record_value, ttl=300):
        """Creates a DNS record in Route 53."""
        try:
            response = self.route53.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': ttl,
                            'ResourceRecords': [{'Value': record_value}],
                        }
                    }]
                }
            )
            logger.info(f"DNS record '{record_name}' created/updated successfully.")
            return response
        except ClientError as e:
            logger.error(f"Failed to create/update DNS record '{record_name}': {e}")
            raise

    # ACM SSL Management
    def request_ssl_certificate(self, domain_name):
        """Requests an SSL certificate for the specified domain."""
        try:
            response = self.acm.request_certificate(
                DomainName=domain_name,
                ValidationMethod='DNS'
            )
            certificate_arn = response['CertificateArn']
            logger.info(f"SSL certificate requested for '{domain_name}'. ARN: {certificate_arn}")
            return certificate_arn
        except ClientError as e:
            logger.error(f"Failed to request SSL certificate for '{domain_name}': {e}")
            raise

    # CloudFront CDN
    def create_cloudfront_distribution(self, bucket_name, domain_name):
        """Creates a CloudFront distribution for an S3 bucket."""
        try:
            response = self.cloudfront.create_distribution(
                DistributionConfig={
                    'CallerReference': str(hash(bucket_name)),
                    'Origins': {
                        'Items': [{
                            'Id': bucket_name,
                            'DomainName': f"{bucket_name}.s3.amazonaws.com",
                            'S3OriginConfig': {'OriginAccessIdentity': ''}
                        }],
                        'Quantity': 1
                    },
                    'DefaultCacheBehavior': {
                        'TargetOriginId': bucket_name,
                        'ViewerProtocolPolicy': 'redirect-to-https',
                        'AllowedMethods': {
                            'Quantity': 2,
                            'Items': ['GET', 'HEAD'],
                            'CachedMethods': {
                                'Quantity': 2,
                                'Items': ['GET', 'HEAD']
                            }
                        },
                        'ForwardedValues': {
                            'QueryString': False,
                            'Cookies': {'Forward': 'none'}
                        },
                        'MinTTL': 0
                    },
                    'Enabled': True
                }
            )
            distribution_id = response['Distribution']['Id']
            logger.info(f"CloudFront distribution created for '{bucket_name}'. ID: {distribution_id}")
            return distribution_id
        except ClientError as e:
            logger.error(f"Failed to create CloudFront distribution for '{bucket_name}': {e}")
            raise
