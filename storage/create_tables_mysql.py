import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

database=app_config['datastore']
db_conn = mysql.connector.connect(host=database['hostname'], user=database['user'],
password=database['password'], database=database['db'])

db_cursor = db_conn.cursor()
db_cursor.execute('''
          CREATE TABLE environment
          (id INT NOT NULL AUTO_INCREMENT, 
           containerId VARCHAR(250) NOT NULL,
           humidity FLOAT NOT NULL,
           lightIntensity FLOAT NOT NULL,
           temperature FLOAT NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           traceid VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT blood_pressure_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE resources
          (id INT NOT NULL AUTO_INCREMENT, 
           containerId VARCHAR(250) NOT NULL,
           electricity FLOAT NOT NULL,
           fertilize FLOAT NOT NULL,
           water FLOAT NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           traceid VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT blood_pressure_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()