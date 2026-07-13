from flask_restful import Resource
import logging
from azReviewer.controller import WebHookController

logger = logging.getLogger(__name__)

class WebHookResource(Resource):

    def get(self):
        """GET endpoint to retrieve configuration"""
        logger.debug("GET /webhook - Configuration request")
        return WebHookController.list_config()
    
    def post(self):
        """POST endpoint to handle Azure DevOps webhook"""
        logger.info("POST /webhook/pipeline - Webhook received")
        return WebHookController.pipeline()
