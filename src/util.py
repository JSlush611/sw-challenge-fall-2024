import os
import logging

def setup_logger(logger_name, log_file, level=logging.INFO):
    """Set up logger with the given name and log file."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:  #
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode='w')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
