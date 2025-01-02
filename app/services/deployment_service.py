import os
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from sqlalchemy.exc import SQLAlchemyError
from app.models.deployment import Deployment
from app.utils.error_handler import handle_db_error

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# AWS SDK Clients
ec2_client = boto3.client("ec2", region_name=os.getenv("AWS_REGION"))
s3_client = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
route53_client = boto3.client("route53", region_name=os.getenv("AWS_REGION"))

class DeploymentService:
    """Service for handling application deployment."""

    @staticmethod
    def create_deployment_record(project_id, user_id, status="pending"):
        """Creates a deployment record in the database."""
        try:
            deployment = Deployment(
                project_id=project_id,
                user_id=user_id,
                status=status
            )
            deployment.save()
            return deployment
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            handle_db_error(e)
            return None

    @staticmethod
    def deploy_to_local(directory, config):
        """Handles local deployment."""
        try:
            logger.info(f"Starting local deployment for {directory}")
            # Mock deployment logic
            # Add real deployment logic like Docker Compose or local setup scripts
            logger.info(f"Successfully deployed {directory} locally")
            return True
        except Exception as e:
            logger.error(f"Error during local deployment: {str(e)}")
            return False

    @staticmethod
    def deploy_to_aws(config):
        """Handles deployment to AWS."""
        try:
            # Provision EC2 instance
            logger.info("Launching EC2 instance...")
            ec2_response = ec2_client.run_instances(
                ImageId=config["ami_id"],
                InstanceType=config["instance_type"],
                MinCount=1,
                MaxCount=1,
                KeyName=config["key_pair"],
                SecurityGroupIds=[config["security_group"]],
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": "Name", "Value": config["project_name"]}]
                    }
                ],
            )
            instance_id = ec2_response["Instances"][0]["InstanceId"]
            logger.info(f"EC2 instance launched: {instance_id}")

            # Configure S3 bucket
            logger.info("Configuring S3 bucket...")
            bucket_name = f"{config['project_name']}-bucket"
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION")},
            )
            logger.info(f"S3 bucket created: {bucket_name}")

            # Configure domain with Route 53
            logger.info("Configuring domain...")
            route53_response = route53_client.change_resource_record_sets(
                HostedZoneId=config["hosted_zone_id"],
                ChangeBatch={
                    "Comment": f"Adding DNS record for {config['domain']}",
                    "Changes": [
                        {
                            "Action": "UPSERT",
                            "ResourceRecordSet": {
                                "Name": config["domain"],
                                "Type": "A",
                                "TTL": 300,
                                "ResourceRecords": [{"Value": config["ec2_public_ip"]}],
                            },
                        }
                    ],
                },
            )
            logger.info(f"Route 53 DNS updated: {route53_response}")

            return True
        except (BotoCoreError, ClientError) as e:
            logger.error(f"AWS deployment error: {str(e)}")
            return False

    @staticmethod
    def rollback_deployment(deployment_id):
        """Rolls back a deployment in case of errors."""
        try:
            logger.info(f"Rolling back deployment {deployment_id}")
            # Mock rollback logic
            # Add real rollback logic, such as terminating EC2 instances or removing S3 buckets
            logger.info(f"Rollback completed for deployment {deployment_id}")
            return True
        except Exception as e:
            logger.error(f"Error during rollback: {str(e)}")
            return False
