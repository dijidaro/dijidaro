
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import current_app as app

def configure_logging(app):
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    handler = RotatingFileHandler("logs/error.log", maxBytes=10000, backupCount=5)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)

    # Attach the file handler to the app's logger
    app.logger.addHandler(handler)
    
    # Optional: Set up a stream handler for console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    app.logger.addHandler(console_handler)

    # Optional: Set a default log level for the app
    app.logger.setLevel(logging.INFO)

    app.logger.info("Logging is configured.")