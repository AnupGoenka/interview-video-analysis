#    
# rq info -u redis://10.0.0.3:6379/

from flask import Flask
from config import *
# from rq.job import Job
from rq import Queue
from redis import Redis
from google.cloud import pubsub

app = Flask(__name__)
app.config.from_object('config')

# redis_conn      = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB_MAIN'])
# redis_conn_rq   = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB_RQ'])

# job_queue = Queue('vision',connection=redis_conn)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config['BASE_DIR'] + "/key.json"

publisher = pubsub.PublisherClient()
# project_id = "ischoolconnect-stage"
# topic     
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id  = app.config['PROJECT_ID'],
    topic       = app.config['TOPIC_NAME'],  # Set this to something appropriate.
)

from vision.api.controllers import *
