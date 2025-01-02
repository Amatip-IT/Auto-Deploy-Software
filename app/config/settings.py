import os

class Config:
    """Base configuration class."""
    # General Configurations
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    DEBUG = False
    TESTING = False

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///development.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Configurations
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # JWT Configurations
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "another-super-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # 1 hour

    # Rate Limiting
    RATELIMIT_HEADERS_ENABLED = True

    # AWS Configurations
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    # OpenAI API Configurations
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class DevelopmentConfig(Config):
    """Development configurations."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    JWT_ACCESS_TOKEN_EXPIRES = 300  # 5 minutes for testing purposes

class ProductionConfig(Config):
    """Production configurations."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///production.db")

# Environment-to-Config mapping
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

# Default configuration
ConfigClass = config_by_name.get(os.getenv("APP_ENV", "development"), DevelopmentConfig)
