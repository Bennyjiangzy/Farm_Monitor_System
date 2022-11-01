import requests
import connexion
import json
from connexion import NoContent
import yaml
import logging
import logging.config
import uuid
import datetime
from pykafka import KafkaClient
from flask_cors import CORS, cross_origin
 

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def report_environment_info(body):
    trace_id=uuid.uuid4()
    body["traceid"]=str(trace_id)
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "environment",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201

def report_resources_info(body):
    trace_id=uuid.uuid4()
    body["traceid"]=str(trace_id)
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "resources",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml",strict_validation=True,validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)