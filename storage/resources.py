from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class Resources(Base):
    """ Resources info """

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    containerId = Column(String(250), nullable=False)
    electricity = Column(Float, nullable=False)
    fertilize = Column(Float, nullable=False)
    water = Column(Float, nullable=False)
    timestamp = Column(String(100), nullable=False)
    traceid = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, containerId, electricity, fertilize, water, timestamp, traceid):
        """ Initializes a resources reading """
        self.containerId = containerId
        self.electricity = electricity
        self.fertilize = fertilize
        self.water = water 
        self.timestamp = timestamp
        self.traceid = traceid
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a resources reading """
        dict = {}
        dict['id'] = self.id
        dict['containerId'] = self.containerId
        dict['electricity'] = self.electricity
        dict['fertilize'] = self.fertilize
        dict['water'] = self.water
        dict['timestamp'] = self.timestamp
        dict['traceid'] = self.traceid
        dict['date_created'] = self.date_created

        return dict
