import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import current_app
from werkzeug.exceptions import BadRequest

class DomainService:
    """Service for managing domain registration and configuration."""

    def __init__(self):
        self.client = boto3.client(
            'route53',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )

    def register_domain(self, domain_name):
        """
        Registers a new domain with AWS Route 53.

        Args:
            domain_name (str): The domain name to register.

        Returns:
            dict: Response from AWS Route 53.

        Raises:
            BadRequest: If domain registration fails.
        """
        try:
            response = self.client.create_hosted_zone(
                Name=domain_name,
                CallerReference=str(hash(domain_name)),
            )
            return response
        except self.client.exceptions.HostedZoneAlreadyExists as e:
            raise BadRequest(f"Domain '{domain_name}' is already registered.") from e
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise BadRequest("AWS credentials are missing or incomplete.") from e
        except Exception as e:
            current_app.logger.error(f"Error registering domain: {e}")
            raise BadRequest("Failed to register domain.") from e

    def configure_dns(self, hosted_zone_id, domain_name, target_dns):
        """
        Configures DNS records for a domain.

        Args:
            hosted_zone_id (str): Hosted zone ID of the domain.
            domain_name (str): Domain name to configure.
            target_dns (str): Target DNS record (e.g., application load balancer).

        Returns:
            dict: Response from AWS Route 53.

        Raises:
            BadRequest: If DNS configuration fails.
        """
        try:
            response = self.client.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Comment': f"Updating DNS records for {domain_name}",
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': domain_name,
                                'Type': 'A',
                                'TTL': 300,
                                'ResourceRecords': [{'Value': target_dns}],
                            },
                        },
                    ],
                },
            )
            return response
        except Exception as e:
            current_app.logger.error(f"Error configuring DNS: {e}")
            raise BadRequest("Failed to configure DNS records.") from e

    def get_hosted_zone(self, domain_name):
        """
        Retrieves the hosted zone information for a domain.

        Args:
            domain_name (str): Domain name to search for.

        Returns:
            dict: Hosted zone information.

        Raises:
            BadRequest: If hosted zone retrieval fails.
        """
        try:
            response = self.client.list_hosted_zones_by_name(DNSName=domain_name)
            hosted_zones = response.get('HostedZones', [])
            for zone in hosted_zones:
                if zone['Name'] == f"{domain_name}.":
                    return zone
            raise BadRequest(f"Hosted zone for '{domain_name}' not found.")
        except Exception as e:
            current_app.logger.error(f"Error retrieving hosted zone: {e}")
            raise BadRequest("Failed to retrieve hosted zone.") from e
