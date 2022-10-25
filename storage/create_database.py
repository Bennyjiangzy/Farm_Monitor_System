import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE environment
          (id INTEGER PRIMARY KEY ASC, 
           containerId VARCHAR(250) NOT NULL,
           humidity FLOAT NOT NULL,
           lightIntensity FLOAT NOT NULL,
           temperature FLOAT NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           traceid VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE resources
          (id INTEGER PRIMARY KEY ASC, 
           containerId VARCHAR(250) NOT NULL,
           electricity FLOAT NOT NULL,
           fertilize FLOAT NOT NULL,
           water FLOAT NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           traceid VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()