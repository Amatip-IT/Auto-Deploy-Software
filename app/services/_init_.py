"""
Initialization for the services module.

This module provides centralized access to various services, including AWS integrations,
deployment workflows, domain management, AI assistance, monitoring, and task scheduling.
"""

from .aws_service import AWSService
from .deployment_service import DeploymentService
from .domain_service import DomainService
from .ai_assistant import AIAssistant
from .monitoring_service import MonitoringService
from .task_scheduler import TaskScheduler
from .notification_service import NotificationService

__all__ = [
    "AWSService",
    "DeploymentService",
    "DomainService",
    "AIAssistant",
    "MonitoringService",
    "TaskScheduler",
    "NotificationService",
]

# Initialize services here if needed
aws_service = AWSService()
deployment_service = DeploymentService()
domain_service = DomainService()
ai_assistant = AIAssistant()
monitoring_service = MonitoringService()
task_scheduler = TaskScheduler()
notification_service = NotificationService()

# Services dictionary for dynamic access
services = {
    "aws_service": aws_service,
    "deployment_service": deployment_service,
    "domain_service": domain_service,
    "ai_assistant": ai_assistant,
    "monitoring_service": monitoring_service,
    "task_scheduler": task_scheduler,
    "notification_service": notification_service,
}
