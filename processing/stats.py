from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class Stats(Base):
    """ Stats info """

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    avg_env_humidity_reading = Column(Float, nullable=False)
    nm_env_recived = Column(Integer, nullable=False)
    avg_env_temp_reading = Column(Float, nullable=False)
    max_env_temp_reading = Column(Float, nullable=False)
    avg_res_elerity_reading = Column(Float, nullable=False)
    avg_res_water_reading = Column(Float, nullable=False)
    max_res_water_reading = Column(Float, nullable=False)
    nm_res_recived = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, avg_env_humidity_reading, nm_env_recived, avg_env_temp_reading, max_env_temp_reading, avg_res_elerity_reading,avg_res_water_reading,max_res_water_reading,nm_res_recived,last_updated):
        """ Initializes a environment reading """
        self.avg_env_humidity_reading = avg_env_humidity_reading
        self.nm_env_recived = nm_env_recived
        self.avg_env_temp_reading = avg_env_temp_reading
        self.max_env_temp_reading = max_env_temp_reading 
        self.avg_res_water_reading = avg_res_water_reading
        self.avg_res_elerity_reading = avg_res_elerity_reading
        self.max_res_water_reading = max_res_water_reading
        self.nm_res_recived = nm_res_recived
        self.last_updated = last_updated
        

    def to_dict(self):
        """ Dictionary Representation of a environment reading """
        dict = {}
        dict['id'] = self.id
        dict['avg_env_humidity_reading'] = self.avg_env_humidity_reading
        dict['nm_env_recived'] = self.nm_env_recived
        dict['avg_env_temp_reading'] = self.avg_env_temp_reading
        dict['max_env_temp_reading'] = self.max_env_temp_reading
        dict['avg_res_water_reading'] = self.avg_res_water_reading
        dict['avg_res_elerity_reading'] = self.avg_res_elerity_reading
        dict['max_res_water_reading'] = self.max_res_water_reading
        dict['nm_res_recived'] = self.nm_res_recived
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")

        return dict
