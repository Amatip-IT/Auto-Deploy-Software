import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database configurations
def get_database_url():
    """
    Constructs the database URL based on environment variables.

    :return: Database URL string
    """
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "auto_deploy_db")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create SQLAlchemy engine and session factory
DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Provides a database session generator for dependency injection.

    :yield: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility to test database connection
def test_database_connection():
    """
    Tests the database connection to ensure it's properly configured.

    :return: None
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
