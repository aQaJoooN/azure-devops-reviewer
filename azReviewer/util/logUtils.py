import json
import logging
from azReviewer.util.azureUtils import AzureGet
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def LogAggregator(pipeline_url):
    """
    Aggregate all logs from an Azure DevOps pipeline build
    
    Args:
        pipeline_url: The base URL of the pipeline build
        
    Returns:
        Dictionary containing log metadata and content
        
    Raises:
        Exception: If logs cannot be retrieved
    """
    logger.info(f"Starting log aggregation for pipeline: {pipeline_url}")
    
    # Get list of logs
    logs_url = pipeline_url + "/logs"
    logger.debug(f"Fetching log list from: {logs_url}")
    
    try:
        response = AzureGet(logs_url)
        logs = response.json()
        
        log_count = len(logs.get("value", []))
        logger.info(f"Found {log_count} log files to download")
        
    except RequestException as e:
        logger.error(f"Failed to retrieve log list from {logs_url}: {str(e)}")
        raise Exception(f"Unable to retrieve logs: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse log list JSON: {str(e)}")
        raise Exception(f"Invalid JSON response from logs endpoint: {str(e)}")

    # Download each log
    successful_downloads = 0
    failed_downloads = 0
    
    for idx, log in enumerate(logs.get("value", []), 1):
        log_id = log.get("id")
        log_url = log.get("url")
        
        logger.debug(f"Downloading log {idx}/{log_count} - ID: {log_id}")
        
        try:
            log_response = AzureGet(log_url)
            
            if log_response.ok:
                log["content"] = log_response.text
                log["content_size"] = len(log_response.text)
                successful_downloads += 1
                logger.debug(f"Log {log_id} downloaded successfully - Size: {log['content_size']} chars")
            else:
                log["content"] = None
                log["download_error"] = log_response.status_code
                failed_downloads += 1
                logger.warning(f"Log {log_id} download failed with status: {log_response.status_code}")
                
        except RequestException as e:
            log["content"] = None
            log["download_error"] = str(e)
            failed_downloads += 1
            logger.error(f"Exception downloading log {log_id}: {str(e)}")
        except Exception as e:
            log["content"] = None
            log["download_error"] = str(e)
            failed_downloads += 1
            logger.error(f"Unexpected error downloading log {log_id}: {str(e)}", exc_info=True)
    
    logger.info(f"Log aggregation complete - Success: {successful_downloads}, Failed: {failed_downloads}")
    
    if successful_downloads == 0 and log_count > 0:
        logger.error("All log downloads failed")
        raise Exception("Failed to download any logs")
    
    return logs
