from flask import Flask
from flask_restful import Api
import logging
from azReviewer.config import Config

import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)


api = Api()

from azReviewer import view

def setup_logging():
    
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    log_level = log_level_map.get(Config.LOG_LEVEL.upper(), logging.WARNING)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set logging for specific libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at {Config.LOG_LEVEL} level")
    return logger

# Application factory
def create_app():
    logger = setup_logging()
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    logger.info(f"Application starting in {Config.ENV} environment")
    logger.debug(f"Configuration - DEBUG: {Config.DEBUG}, TESTING: {Config.TESTING}, TIMEOUT: {Config.TIMEOUT}, RETRY: {Config.RETRY}")
    
    api.init_app(app)
    
    logger.info("Application initialized successfully")
    return app
