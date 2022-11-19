import yaml
import json
from logging import config
import logging.config
import connexion
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
from connexion import NoContent
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import sqlite3
from base import Base
from status import Status

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, "r") as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger("basicLogger")

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

database=app_config['datastore']

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
DATA_FILE=app_config['datastore']['filename']

def get_status():
    logger.info("request get has made")
    if not os.path.isfile(DATA_FILE):
        logger.error("Status does not exist creating now")
        return "Status does not exist", 404

    session = DB_SESSION()
    results = session.query(Status).order_by(Status.last_update.desc())
    session.close()

    if len(results.all()) == 0:
        logger.error("Statistics does not exist")
        return "Statistics does not exist", 404
    latest_data=results[0].to_dict()
    logger.debug(f"data get{latest_data}")
    logger.info("request is complete")
    return latest_data, 200

def show_data():
    session = DB_SESSION()
    results = session.query(Status).order_by(Status.last_update.desc())
    session.close()
    if len(results.all()) !=0:
        return results[0].to_dict()
    return {'receiver':"Down",'storage':"Down",'processing':"Down",'audit':"Down",'last_update':"0",}

def populate_status():
    logger.info("A Health check begins")
    current_data = show_data()
    
    try:
        response_audit=requests.get(app_config['audit']['url'], timeout=app_config['timeout'])
        if response_audit.status_code == 200:
            current_data['audit'] = "Running"
            logger.info("audit service is running")
    except:
        current_data['audit'] = "Down"
        logger.info("audit service is down")

    try:
        response_processing=requests.get(app_config['processing']['url'], timeout=app_config['timeout'])
        if response_processing.status_code == 200:
            current_data['processing'] = "Running"
            logger.info("processing service is running")
    except:
        current_data['processing'] = "Down"
        logger.info("processing service is down")

    try:
        response_receiver=requests.get(app_config['receiver']['url'], timeout=app_config['timeout'])
        if response_receiver.status_code == 200:
            current_data['receiver'] = "Running"
            logger.info("receiver service is running")
    except:
        current_data['receiver'] = "Down"
        logger.info("receiver service is down")

    try:
        response_storage=requests.get(app_config['storage']['url'], timeout=app_config['timeout'])
        if response_storage.status_code == 200:
            current_data['storage'] = "Running"
            logger.info("storage service is running")
    except:
        current_data['storage'] = "Down"
        logger.info("storage service is down")

    current_time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    session = DB_SESSION()
    status_data=Status(
                    current_data['receiver'],
                    current_data['storage'],
                    current_data['processing'],
                    current_data['audit'],
                    datetime.datetime.strptime(str(current_time),"%Y-%m-%dT%H:%M:%SZ")
                )
    session.add(status_data)
    session.commit()
    session.close()
    logger.info(f"Status sql updated time{current_time}")
    logger.info("A Health check end")
    
def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_status, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml",strict_validation=True,validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8120, use_reloader=False)