
from os import environ

class Config:

    ENV = environ.get("AZR_ENV", "production")

    DEBUG = int(environ.get("AZR_DEBUG", "0"))

    TESTING = int(environ.get("AZR_TESTING", "0"))

    TIMEOUT = int(environ.get("AZR_TIMEOUT", "30"))

    RETRY = int(environ.get("AZR_RETRY", "5"))

    LOG_LEVEL = environ.get("AZR_LOG_LEVEL", "WARN") # DEBUG, INFO, WARN, ERROR

    ########## Azure DevOps ##########
    
    AZURE_TOKEN = environ.get("AZR_AZURE_TOKEN","")

    ########## AI Endpoint ##########

    AI_URL = environ.get("AZR_AI_URL","")
    
    AI_KEY = environ.get("AZR_AI_KEY","")

