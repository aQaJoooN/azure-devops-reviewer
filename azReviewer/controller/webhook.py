from flask import abort, request, jsonify
import logging
from azReviewer.config import Config
import json
from azReviewer.util import LogAggregator

logger = logging.getLogger(__name__)

class WebHookController:
    def pipeline():
        """
        Handle Azure DevOps build completion webhook
        """
        logger.info("Received webhook request")
        
        # Validate content type
        if request.content_type != "application/json; charset=utf-8":
            logger.warning(f"Invalid content type: {request.content_type}")
            abort(415)
        
        # Parse JSON data
        try:
            data = request.get_json()
        except Exception as e:
            logger.error(f"Failed to parse JSON data: {str(e)}")
            abort(400)

        if not data:
            logger.warning("Empty request body received")
            abort(400)

        # Log incoming event details
        event_type = data.get("eventType")
        logger.debug(f"Webhook event type: {event_type}")
        
        if event_type != "build.complete":
            logger.info(f"Ignoring event type: {event_type} (not build.complete)")
            abort(400)
        
        # Extract build information
        resource = data.get("resource", {})
        build_id = resource.get("id")
        build_number = resource.get("buildNumber")
        log_url = resource.get("url")
        
        logger.info(f"Processing build completion - ID: {build_id}, Number: {build_number}")
        logger.debug(f"Build URL: {log_url}")
        
        if not log_url:
            logger.error("Build URL not found in webhook payload")
            abort(400)
        
        # Aggregate logs
        try:
            log_content = LogAggregator(log_url)
            logger.info(f"Successfully aggregated logs for build {build_number}")
            logger.debug(f"Retrieved {len(log_content.get('value', []))} log entries")
            
            # TODO: Send logs to AI API for review
            # TODO: Add review as markdown to Azure pipeline
            
            return {"status": "success", "build_id": build_id, "message": "Logs processed successfully"}, 200
            
        except Exception as e:
            logger.error(f"Failed to aggregate logs for build {build_number}: {str(e)}", exc_info=True)
            return {"status": "error", "message": "Failed to process build logs"}, 500
    
    def list_config():
        """
        Return application configuration (for debugging)
        """
        logger.debug("Configuration requested")
        
        # Mask sensitive information
        masked_ai_url = Config.AI_URL[:20] + "..." if len(Config.AI_URL) > 20 else Config.AI_URL
        
        return {
            "AI_URL": masked_ai_url,
            "LOG_LEVEL": Config.LOG_LEVEL,
            "RETRY": Config.RETRY, 
            "TIMEOUT": Config.TIMEOUT, 
            "TESTING": Config.TESTING, 
            "DEBUG": Config.DEBUG, 
            "ENV": Config.ENV
        }
