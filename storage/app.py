from pydoc_data.topics import topics
import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import yaml
import logging
import logging.config
import datetime
from environment import Environment
from resources import Resources
from threading import Thread
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json
from flask_cors import CORS, cross_origin
from sqlalchemy import and_
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable
import time
import pymysql

from environment import Environment
from resources import Resources

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

database=app_config['datastore']

logger.info(f"Connect to DB. Hostname: {database['hostname']}, PORT: {database['port']}")
DB_ENGINE= create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(database['user'],database['password'],database['hostname'],database['port'],database['db']))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_environment_info(timestamp,end_timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(Environment).filter(and_(Environment.date_created >= timestamp_datetime, Environment.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for environment info after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200


def get_resources_info(timestamp,end_timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(Resources).filter(and_(Resources.date_created >= timestamp_datetime, Resources.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for resources info readings after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    maxtry=0
    while maxtry <  app_config["kafka"]["maxtry"]:
        client = KafkaClient(hosts=hostname)
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                            reset_offset_on_start=False,
                                            auto_offset_reset=OffsetType.LATEST)
        try:
            logger.info(f'Trying to connect to the Kafka. Current try: {maxtry}')
            consumer.consume()
        except (SocketDisconnectedError) as e:
            logger.error(f"Can't connect to the kafka. Current try: {maxtry}")
            consumer.stop()
            consumer.start()
            time.sleep(app_config["kafka"]["sleep"])
        maxtry+=1




    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]
        logger.info(payload)

        if msg["type"] == "environment":
            session = DB_SESSION()
            logger.info(f'Connected to database at {app_config["datastore"]["hostname"]}')

            environment = Environment(payload['containerId'],
                       payload['humidity'],
                       payload['lightIntensity'],
                       payload['temperature'],
                       payload['timestamp'],
                       payload['traceid'])

            session.add(environment)

            session.commit()
            session.close()
            logger.info(f"Connecting to DB. Hostname:{database['hostname']}, Port:3306")

        elif msg["type"] == "resources":
            session = DB_SESSION()

            resources = Resources(payload['containerId'],
                       payload['electricity'],
                       payload['fertilize'],
                       payload['water'],
                       payload['timestamp'],
                       payload['traceid'])

            session.add(resources)

            session.commit()
            session.close()
            logger.info(f"Connecting to DB. Hostname:{database['hostname']}, Port:3306")
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml",strict_validation=True,validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)



# grant all privileges on events.* to 'root'@'%';