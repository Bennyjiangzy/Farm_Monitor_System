import sqlite3
import yaml
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

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