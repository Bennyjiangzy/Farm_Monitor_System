import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

database=app_config['datastore']
db_conn = mysql.connector.connect(host=database['hostname'], user=database['user'],
password=database['password'], database=database['db'])

db_cursor = db_conn.cursor()
db_cursor.execute('''
          DROP TABLE IF EXISTS environment;
          ''')

db_cursor.execute('''
          DROP TABLE IF EXISTS resources;
          ''')

db_conn.commit()
db_conn.close()