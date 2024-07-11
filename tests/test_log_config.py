# log_config.py
import logging


def setup_logging():
    logger = logging.getLogger('dummy_logger')
    logger.setLevel(logging.CRITICAL)  # Set logger level to CRITICAL to ignore INFO messages
    logger.addHandler(logging.NullHandler())
    return logger

# Create a global logger instance
logger = setup_logging()