import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """
        Clean up previous handlers from the root logger
        Initialize the root logging with basic config:
            - Logging level: INFO
            - Handlers: StreamHandler (Console), RotatingFileHandler (File)
            - Backup count: 5
    """
    logging.root.handlers.clear()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(name)s: %(message)s",
                        handlers=[
                            logging.StreamHandler(),
                            RotatingFileHandler("/src/logs/drivenow.log", maxBytes=100_000, backupCount=5)
                        ])
