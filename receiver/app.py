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
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable
import time
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)
logger.info(f"test {log_conf_file['handlers']['file']}")

maxtry=0
while maxtry <  app_config["kafka"]["maxtry"]:
    try:
        logger.info(f'Trying to connect to the Kafka producer. Current try: {maxtry}')
        client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
        topic = client.topics[str.encode(app_config['events']["topic"])]
        producer = topic.get_sync_producer()
        break
    except Exception as e:
        logger.error(f"Can't connect to the kafka producer. Current try: {maxtry}")
        time.sleep(app_config["kafka"]["sleep"])
    maxtry+=1

def report_environment_info(body):
    trace_id=uuid.uuid4()
    body["traceid"]=str(trace_id)
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