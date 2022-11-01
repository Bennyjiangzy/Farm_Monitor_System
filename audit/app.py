import yaml
from pykafka import KafkaClient
import json
from logging import config
import logging.config
import connexion
from flask_cors import CORS, cross_origin


with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())
    kafka_info = app_config["events"]

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger("basicLogger")


def get_environment_index(index):
    client = KafkaClient(hosts='%s:%d' % (app_config["events"]["hostname"], app_config["events"]["port"]))
    topic = client.topics[str.encode(kafka_info["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving customer orders at index %d" % index)

    count = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'environment':
                if count == index:
                    return msg['payload'], 200
                count += 1
    except:

        logger.error("No more messages found")
    logger.error("Could not find environment at index %d" % index)

    return {"message": "Not Found"}, 404


def get_resources_index(index):
    client = KafkaClient(hosts='%s:%d' % (app_config["events"]["hostname"], app_config["events"]["port"]))
    topic = client.topics[str.encode(kafka_info["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving resources at index %d" % index)

    count = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'resources':
                if count == index:
                    return msg['payload'], 200
                count += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find completed orders at index %d" % index)

    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml",strict_validation=True,validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110)