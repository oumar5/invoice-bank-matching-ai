import logging
import sys
from config.settings import LOG_LEVEL, LOG_FORMAT

def setup_logger(name):
    """
    Configure un logger avec un format spécifique et des handlers pour la console
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)

    # Configuration du logger
    logger.handlers = []
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger 