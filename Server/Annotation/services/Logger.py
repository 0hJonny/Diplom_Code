import logging

class Logger:
    def __init__(self):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.error_logger = logging.getLogger("error_logger")

        # Create handlers
        articles_handler = logging.FileHandler("logs/Articles.log")
        articles_handler.setLevel(logging.INFO)
        error_handler = logging.FileHandler("logs/Error.log")
        error_handler.setLevel(logging.ERROR)

        # Create formatter and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        articles_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        # Add handlers to loggers
        self.logger.addHandler(articles_handler)
        self.error_logger.addHandler(error_handler)

    def info(self, message):
        # Log info message
        self.logger.info(message)

    def error(self, message):
        # Log error message
        self.error_logger.error(message)
