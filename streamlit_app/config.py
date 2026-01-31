"""
Streamlit configuration and setup
"""

import os
from pathlib import Path

# Get the streamlit app directory
STREAMLIT_DIR = Path(__file__).parent

# Environment variables
SCYLLA_HOST = os.getenv("SCYLLA_HOST", "scylla-node")
SCYLLA_PORT = int(os.getenv("SCYLLA_PORT", "9042"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Application settings
APP_NAME = "Hospital Management System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A comprehensive Python-based healthcare management platform"

# Feature flags
FEATURES = {
    'patient_registration': True,
    'patient_search': True,
    'dashboard': True,
    'advanced_analytics': False,  # Coming soon
    'appointments': False,  # Coming soon
    'prescriptions': False,  # Coming soon
}

# Cache configuration
CACHE_TTL = 300  # 5 minutes

# Pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%B %d, %Y"
DISPLAY_DATETIME_FORMAT = "%B %d, %Y at %H:%M"

# Error messages
ERROR_MESSAGES = {
    'db_connection': 'Unable to connect to database. Please check your database configuration.',
    'invalid_data': 'Invalid data provided. Please check your input.',
    'patient_not_found': 'Patient not found in the system.',
    'operation_failed': 'Operation failed. Please try again.',
}

# Success messages
SUCCESS_MESSAGES = {
    'patient_created': 'Patient registered successfully!',
    'patient_updated': 'Patient information updated successfully!',
    'patient_deleted': 'Patient record deleted successfully!',
}
