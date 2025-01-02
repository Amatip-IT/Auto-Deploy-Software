from celery import Celery
from datetime import datetime, timedelta
import logging

# Celery configuration
celery_app = Celery('task_scheduler', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Configure Celery
celery_app.conf.update(
    timezone='UTC',
    enable_utc=True,
    task_annotations={
        '*': {'rate_limit': '10/s'}  # Rate limit for tasks
    },
    result_expires=3600  # Task results expire after 1 hour
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TaskScheduler')

@celery_app.task(bind=True)
def clear_old_logs(self):
    """
    A task to clear old logs from the system.
    """
    try:
        logger.info("Starting log cleanup...")
        # Logic to delete logs older than a specific duration
        # Example: Delete files from a log directory
        # You can replace this with your log cleanup logic
        logger.info("Old logs cleared successfully.")
    except Exception as e:
        logger.error(f"Failed to clear logs: {str(e)}")

@celery_app.task(bind=True)
def send_email_reminders(self):
    """
    A task to send email reminders to users.
    """
    try:
        logger.info("Starting email reminders...")
        # Logic to send email reminders
        # Example: Fetch users with pending notifications
        logger.info("Email reminders sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email reminders: {str(e)}")

@celery_app.task(bind=True)
def optimize_database(self):
    """
    A task to optimize the database by running maintenance operations.
    """
    try:
        logger.info("Starting database optimization...")
        # Logic for database optimization
        # Example: Vacuum and analyze for PostgreSQL
        logger.info("Database optimized successfully.")
    except Exception as e:
        logger.error(f"Failed to optimize the database: {str(e)}")

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Configures periodic tasks using Celery's beat scheduler.
    """
    # Clear old logs every day at midnight
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        clear_old_logs.s(),
        name='Clear old logs every midnight'
    )

    # Send email reminders every hour
    sender.add_periodic_task(
        crontab(minute=0),
        send_email_reminders.s(),
        name='Send email reminders every hour'
    )

    # Optimize database every Sunday at 3 AM
    sender.add_periodic_task(
        crontab(hour=3, minute=0, day_of_week=6),
        optimize_database.s(),
        name='Optimize database weekly'
    )

# Manual Task Invocation (Optional)
def run_task(task_name):
    """
    Manually run a specific task by name.
    """
    task_mapping = {
        'clear_old_logs': clear_old_logs,
        'send_email_reminders': send_email_reminders,
        'optimize_database': optimize_database,
    }
    task = task_mapping.get(task_name)
    if task:
        logger.info(f"Running task: {task_name}")
        task.delay()
    else:
        logger.error(f"Task '{task_name}' not found.")
