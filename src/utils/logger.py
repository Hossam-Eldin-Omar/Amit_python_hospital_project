"""Logging configuration for the hospital application"""
import logging
import sys
from datetime import datetime


def setup_logger(name: str, level=logging.INFO):
    """
    Setup and return a logger with the given name.

    Args:
        name: Logger name (usually __name__ of the module)
        level: Logging level (default: INFO)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        # fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        # datefmt='%Y-%m-%d %H:%M:%S'
        fmt="%(message)s"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Create a default logger for the application
default_logger = setup_logger("hospital_app")
