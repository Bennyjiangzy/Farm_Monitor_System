from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class Environment(Base):
    """ Environment info """

    __tablename__ = "environment"

    id = Column(Integer, primary_key=True)
    containerId = Column(String(250), nullable=False)
    humidity = Column(Float, nullable=False)
    lightIntensity = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    timestamp = Column(String(100), nullable=False)
    traceid = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, containerId, humidity, lightIntensity, temperature, timestamp,traceid):
        """ Initializes a environment reading """
        self.containerId = containerId
        self.humidity = humidity
        self.lightIntensity = lightIntensity
        self.temperature = temperature 
        self.timestamp = timestamp
        self.traceid = traceid
        self.date_created = datetime.datetime.now()
        

    def to_dict(self):
        """ Dictionary Representation of a environment reading """
        dict = {}
        dict['id'] = self.id
        dict['containerId'] = self.containerId
        dict['humidity'] = self.humidity
        dict['lightIntensity'] = self.lightIntensity
        dict['temperature'] = self.temperature
        dict['timestamp'] = self.timestamp
        dict['traceid'] = self.traceid
        dict['date_created'] = self.date_created

        return dict
