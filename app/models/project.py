from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Project(Base):
    """
    Model representing a project.
    Each project is associated with a user and contains information like name, description, status, etc.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="Pending")  # E.g., Pending, Deployed, Failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="projects")

    # Deployment-related fields
    deployment_url = Column(String(500), nullable=True)
    deployment_logs = Column(Text, nullable=True)
    is_live = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Project(name={self.name}, status={self.status}, user_id={self.user_id})>"

    def to_dict(self):
        """
        Convert the project object to a dictionary for easier serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deployment_url": self.deployment_url,
            "deployment_logs": self.deployment_logs,
            "is_live": self.is_live,
            "user_id": self.user_id,
        }