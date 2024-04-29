import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.error_logger = logging.getLogger("error_logger")

        # Create handlers
        articles_handler = RotatingFileHandler("logs/Articles.log", maxBytes=1000000, backupCount=5)
        error_handler = RotatingFileHandler("logs/Error.log", maxBytes=1000000, backupCount=5)

        # Create formatter and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        articles_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        # Add handlers to loggers
        self.logger.addHandler(articles_handler)
        self.error_logger.addHandler(error_handler)

        # Enable logging to file
        self.logger.propagate = False
        self.error_logger.propagate = False

    def info(self, message):
        # Log info message
        self.logger.info(message)

    def error(self, message):
        # Log error message
        self.error_logger.error(message)



