import psutil
import datetime
import redis
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.logs import Log  # Assuming a Log model exists
from app.utils.helpers import handle_db_error

# Initialize Redis connection
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringService:
    """Service for monitoring and reporting system and application status."""

    @staticmethod
    def get_system_metrics():
        """
        Fetches system-level metrics like CPU and memory usage.
        
        Returns:
            dict: System metrics including CPU and memory usage.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            
            metrics = {
                "cpu_usage": f"{cpu_usage}%",
                "memory_usage": f"{memory_info.percent}%",
                "disk_usage": f"{disk_usage.percent}%",
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
            return metrics
        except Exception as e:
            logger.error(f"Error fetching system metrics: {e}")
            return {"error": "Failed to fetch system metrics"}

    @staticmethod
    def fetch_deployment_logs(deployment_id):
        """
        Fetches logs for a specific deployment.
        
        Args:
            deployment_id (str): The ID of the deployment.

        Returns:
            list: Logs related to the deployment.
        """
        try:
            logs = Log.query.filter_by(deployment_id=deployment_id).order_by(Log.timestamp.desc()).all()
            return [log.to_dict() for log in logs]
        except SQLAlchemyError as e:
            handle_db_error(e)
            return {"error": "Failed to fetch deployment logs"}

    @staticmethod
    def get_live_updates(key_prefix):
        """
        Fetches live updates from Redis.
        
        Args:
            key_prefix (str): Prefix of the Redis key to monitor.

        Returns:
            dict: Live data updates.
        """
        try:
            keys = redis_client.keys(f"{key_prefix}*")
            updates = {key: redis_client.get(key) for key in keys}
            return updates
        except Exception as e:
            logger.error(f"Error fetching live updates: {e}")
            return {"error": "Failed to fetch live updates"}

    @staticmethod
    def monitor_errors():
        """
        Monitors and fetches application-level errors.
        
        Returns:
            list: List of application errors.
        """
        try:
            errors = Log.query.filter_by(level="ERROR").order_by(Log.timestamp.desc()).all()
            return [error.to_dict() for error in errors]
        except SQLAlchemyError as e:
            handle_db_error(e)
            return {"error": "Failed to fetch error logs"}

    @staticmethod
    def save_metric_to_db(metric_data):
        """
        Saves metric data to the database for historical analysis.
        
        Args:
            metric_data (dict): Metric data to save.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            new_log = Log(
                level="INFO",
                message=str(metric_data),
                timestamp=datetime.datetime.utcnow(),
            )
            db.session.add(new_log)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            handle_db_error(e)
            return False
