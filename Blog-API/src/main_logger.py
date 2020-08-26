import logging
from logging.handlers import TimedRotatingFileHandler
import logging.config
import sys

FORMATTER = logging.Formatter(f"[%(levelname)s]: [%(asctime)s] [%(lineno)d] [%(filename)s] [%(message)s]")
LOG_FILE = "service.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)
    return console_handler

def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.INFO)
    return file_handler


def set_up_logging():
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        logger.addHandler(get_console_handler())
        logger.addHandler(get_file_handler())
        logger.propagate = False
    return logger