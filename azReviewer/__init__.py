from flask import Flask
from flask_restful import Api
import logging
from azReviewer.config import Config

import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)


api = Api()

from azReviewer import view

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Application factory
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # Load configs from ENV variables.
    api.init_app(app)
    return app