from datetime import datetime
from ..database import db

class Deployment(db.Model):
    """
    Model representing deployment data.
    """
    __tablename__ = 'deployments'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    repository_url = db.Column(db.String(255), nullable=False)
    branch = db.Column(db.String(100), default="main")
    deployment_status = db.Column(db.String(50), default="Pending")
    deployed_url = db.Column(db.String(255), nullable=True)
    logs = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, project_name, user_id, repository_url, branch="main"):
        """
        Initialize a Deployment instance.

        :param project_name: Name of the project being deployed
        :param user_id: ID of the user initiating the deployment
        :param repository_url: URL of the repository for the project
        :param branch: Branch to be deployed (default: "main")
        """
        self.project_name = project_name
        self.user_id = user_id
        self.repository_url = repository_url
        self.branch = branch

    def to_dict(self):
        """
        Serialize the deployment object to a dictionary.

        :return: Dictionary representation of the deployment
        """
        return {
            "id": self.id,
            "project_name": self.project_name,
            "user_id": self.user_id,
            "repository_url": self.repository_url,
            "branch": self.branch,
            "deployment_status": self.deployment_status,
            "deployed_url": self.deployed_url,
            "logs": self.logs,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update_status(self, status, deployed_url=None, logs=None):
        """
        Update the status, deployed URL, and logs of the deployment.

        :param status: New deployment status (e.g., "In Progress", "Completed", "Failed")
        :param deployed_url: URL where the deployment is accessible (optional)
        :param logs: Deployment logs (optional)
        """
        self.deployment_status = status
        if deployed_url:
            self.deployed_url = deployed_url
        if logs:
            self.logs = logs
