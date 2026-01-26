import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class DatabaseConfig:
    """Database configuration settings"""

    SCYLLA_HOSTS = os.getenv("SCYLLA_HOSTS", "172.17.0.2").split(",")
    SCYLLA_PORT = int(os.getenv("SCYLLA_PORT", "9042"))
    SCYLLA_KEYSPACE = os.getenv("SCYLLA_KEYSPACE", "hospital_db")
    SCYLLA_REPLICATION_FACTOR = int(os.getenv("SCYLLA_REPLICATION_FACTOR", "1"))


class AppConfig:
    """Application configuration settings"""

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")


class Config:
    """Main configuration class"""

    DB = DatabaseConfig()
    APP = AppConfig()
