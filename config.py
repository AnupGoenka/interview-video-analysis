# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY      = "secret"
REDIS_HOST      = '127.0.0.1'
REDIS_PORT      = '6379'
REDIS_DB_MAIN   = '0'
# REDIS_DB_RQ     = '1'

# PUBSUB CREDENTIALS
PROJECT_ID = 'ischoolconnect-stage'
TOPIC_NAME = 'video-analysis'