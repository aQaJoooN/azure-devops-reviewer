import requests
import logging
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError, Timeout
from azReviewer.config import Config

logger = logging.getLogger(__name__)

def AzureGet(url, retry_count=0):
    """
    Make authenticated GET request to Azure DevOps API
    
    Args:
        url: The Azure DevOps API URL to call
        retry_count: Current retry attempt number
        
    Returns:
        Response object
        
    Raises:
        HTTPError: If the request fails after all retries
    """
    max_retries = Config.RETRY
    timeout = Config.TIMEOUT
    
    logger.debug(f"Making Azure API request to: {url}")
    
    try:
        session = requests.Session()
        session.auth = HTTPBasicAuth("", Config.AZURE_TOKEN)
        session.verify = False  # Disable SSL verification for on-premise Azure DevOps
        
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        
        logger.debug(f"Azure API request successful - Status: {response.status_code}, Size: {len(response.content)} bytes")
        return response
        
    except Timeout as e:
        logger.error(f"Request timeout after {timeout}s for URL: {url}")
        if retry_count < max_retries:
            logger.info(f"Retrying request ({retry_count + 1}/{max_retries})...")
            return AzureGet(url, retry_count + 1)
        else:
            logger.error(f"Max retries ({max_retries}) reached for URL: {url}")
            raise
            
    except HTTPError as e:
        logger.error(f"HTTP error {e.response.status_code} for URL: {url} - {str(e)}")
        if retry_count < max_retries and e.response.status_code >= 500:
            logger.info(f"Retrying request after server error ({retry_count + 1}/{max_retries})...")
            return AzureGet(url, retry_count + 1)
        else:
            raise
            
    except RequestException as e:
        logger.error(f"Request failed for URL: {url} - {str(e)}")
        if retry_count < max_retries:
            logger.info(f"Retrying request ({retry_count + 1}/{max_retries})...")
            return AzureGet(url, retry_count + 1)
        else:
            logger.error(f"Max retries ({max_retries}) reached for URL: {url}")
            raise
            
    except Exception as e:
        logger.error(f"Unexpected error calling Azure API: {str(e)}", exc_info=True)
        raise
