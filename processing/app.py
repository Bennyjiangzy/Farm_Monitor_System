import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml
import logging
import logging.config
import datetime
from base import Base
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from stats import Stats
import os
from flask_cors import CORS, cross_origin
import sqlite3

LAST_UPDATED_default="2016-08-29T09:12:33Z"


if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

database=app_config['datastore']

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
DATA_FILE=app_config['datastore']['filename']
if not os.path.isfile(DATA_FILE):
    conn = sqlite3.connect(app_config['datastore']['filename'])


    c = conn.cursor()
    c.execute('''
            CREATE TABLE stats
            (id INTEGER PRIMARY KEY ASC, 
            avg_env_humidity_reading FLOAT NOT NULL,
            nm_env_recived INTEGER NOT NULL,
            avg_env_temp_reading FLOAT NOT NULL,
            max_env_temp_reading FLOAT NOT NULL,
            avg_res_elerity_reading FLOAT NOT NULL,
            avg_res_water_reading FLOAT NOT NULL,
            max_res_water_reading FLOAT NOT NULL,
            nm_res_recived INTEGER NOT NULL,
            last_updated VARCHAR(100) NOT NULL)
            ''')

    conn.commit()
    conn.close()
    logger.info("Statistics create complete")

def get_stats():
    logger.info("request get has made")
    if not os.path.isfile(DATA_FILE):
        logger.error("Statistics does not exist creating now")
        conn = sqlite3.connect(app_config['datastore']['filename'])


        c = conn.cursor()
        c.execute('''
                CREATE TABLE stats
                (id INTEGER PRIMARY KEY ASC, 
                avg_env_humidity_reading FLOAT NOT NULL,
                nm_env_recived INTEGER NOT NULL,
                avg_env_temp_reading FLOAT NOT NULL,
                max_env_temp_reading FLOAT NOT NULL,
                avg_res_elerity_reading FLOAT NOT NULL,
                avg_res_water_reading FLOAT NOT NULL,
                max_res_water_reading FLOAT NOT NULL,
                nm_res_recived INTEGER NOT NULL,
                last_updated VARCHAR(100) NOT NULL)
                ''')

        conn.commit()
        conn.close()
        logger.info("Statistics create complete")
        return "Statistics does not exist", 404

    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    session.close()

    if len(results.all()) == 0:
        logger.error("Statistics does not exist")
        return "Statistics does not exist", 404
    latest_data=results[0].to_dict()
    logger.debug(f"data get{latest_data}")
    logger.info("request is complete")
    return latest_data, 200

def env_data(data,nm):
    env_data = {"avg_env_humidity_reading":0,
                "nm_env_recived":nm,
                "avg_env_temp_reading":0,
                "max_env_temp_reading":0}
    if data == []:
        return env_data
        
    avg_humidity=0
    nm_events=len(data)+nm
    avg_temp=0
    max_temp=data[0]['temperature']

    for i in data:
        avg_humidity+=i['humidity']
        avg_temp+=i['temperature']
        max_temp = max(max_temp,i['temperature'])
        logger.debug(f"The env data has been processed with trace_id {i['traceid']}")

    env_data['avg_env_humidity_reading'] = avg_humidity/nm_events
    env_data['nm_env_recived'] = nm_events
    env_data['avg_env_temp_reading'] = avg_temp/nm_events
    env_data['max_env_temp_reading'] = max_temp
    return env_data

def res_data(data,nm):
    res_data = {"avg_res_elerity_reading":0,
                "avg_res_water_reading":0,
                "max_res_water_reading":0,
                "nm_res_recived":nm}
    if data == []:
        return res_data

    avg_elerity=0
    nm_events=len(data)+nm
    avg_water=0
    max_water=data[0]['water']

    for i in data:
        avg_elerity+=i['electricity']
        avg_water+=i['water']
        max_water = max(max_water,i['water'])
        logger.debug(f"The res data has been processed with trace_id {i['traceid']}")

    res_data['avg_res_elerity_reading'] = avg_elerity/nm_events
    res_data['avg_res_water_reading'] = avg_water/nm_events
    res_data['max_res_water_reading'] = max_water
    res_data['nm_res_recived'] = nm_events
    return res_data

def show_lasttime():
    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    session.close()
    if len(results.all()) !=0:
        return results[0].to_dict()
    return {'last_updated':LAST_UPDATED_default,'nm_res_recived':0,'nm_env_recived':0}

def populate_stats():
    """ Periodically update stats """
    logger.info("Start Periodic Processing")
    
    # #read data from sqlite
    Last_update=show_lasttime()
    current_time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    # get data from storage by get environment
    response_env = requests.get(app_config['eventstore1']['url']+f"?timestamp={Last_update['last_updated']}&end_timestamp={current_time}")
    if response_env.status_code == 200:
        logger.info(f'{len(response_env.json())} env info recived with status {response_env.status_code}')
    else:
        logger.error(f'Cannot get the env info with status {response_env.status_code}')

    response_res = requests.get(app_config['eventstore2']['url']+f"?timestamp={Last_update['last_updated']}&end_timestamp={current_time}")
    if response_res.status_code == 200:
        logger.info(f'{len(response_env.json())} res info recived with status {response_res.status_code}')
    else:
        logger.error(f'Cannot get the res info with status {response_res.status_code}')

    # process data
    processed_env=env_data(response_env.json(),Last_update['nm_env_recived'])
    processed_res=res_data(response_res.json(),Last_update['nm_res_recived'])

    # #write data to sqlite
    session = DB_SESSION()
    
    stats_data=Stats(
                    processed_env['avg_env_humidity_reading'],
                    processed_env['nm_env_recived'],
                    processed_env['avg_env_temp_reading'],
                    processed_env['max_env_temp_reading'],
                    processed_res['avg_res_elerity_reading'],
                    processed_res['avg_res_water_reading'],
                    processed_res['max_res_water_reading'],
                    processed_res['nm_res_recived'],
                    datetime.datetime.strptime(str(current_time),"%Y-%m-%dT%H:%M:%SZ")
                )

    session.add(stats_data)
    session.commit()
    session.close()
    logger.info(f"Stats update {processed_env['nm_env_recived']} data env info got, avg humidity: {processed_env['avg_env_humidity_reading']} avg temperature: {processed_env['avg_env_temp_reading']} max tempreature: {processed_env['max_env_temp_reading']}. {processed_res['nm_res_recived']} data res got, avg elerity: {processed_res['avg_res_elerity_reading']}, avg water: {processed_res['avg_res_water_reading']}, max water: {processed_res['max_res_water_reading']}")
    logger.info("Start Periodic end")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml",strict_validation=True,validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100,use_reloader=False)