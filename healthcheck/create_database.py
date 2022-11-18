import sqlite3
import yaml
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

conn = sqlite3.connect(app_config['datastore']['filename'])


c = conn.cursor()
c.execute('''
          CREATE TABLE status
          (id INTEGER PRIMARY KEY ASC, 
           receiver VARCHAR(100) NOT NULL,
           storage VARCHAR(100) NOT NULL,
           processing VARCHAR(100) NOT NULL,
           audit VARCHAR(100) NOT NULL,
           last_update VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()