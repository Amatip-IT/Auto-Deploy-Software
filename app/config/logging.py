import logging
import os
from logging.handlers import RotatingFileHandler

# Define the log directory and file
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Logging Levels
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

# Formatter for logs
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# File Handler
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5  # 5MB per log file, 5 backups
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(formatter)

# Root Logger Configuration
logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[file_handler, console_handler]
)

def get_logger(name):
    """
    Retrieves a logger with the specified name.

    :param name: Name of the logger
    :return: Configured logger instance
    """
    return logging.getLogger(name)

# Example Usage
if __name__ == "__main__":
    logger = get_logger("test_logger")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")