from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime

class Status(Base):
    """ Stats info """

    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    receiver = Column(String, nullable=False)
    storage = Column(String, nullable=False)
    processing = Column(String, nullable=False)
    audit = Column(String, nullable=False)
    last_update = Column(DateTime, nullable=False)

    def __init__(self, receiver, storage, processing, audit, last_update):
        """ Initializes a environment reading """
        self.receiver = receiver
        self.storage = storage
        self.processing = processing
        self.audit = audit 
        self.last_update = last_update
        

    def to_dict(self):
        """ Dictionary Representation of a environment reading """
        dict = {}
        dict['id'] = self.id
        dict['receiver'] = self.receiver
        dict['storage'] = self.storage
        dict['processing'] = self.processing
        dict['audit'] = self.audit
        dict['last_update'] = self.last_update.strftime("%Y-%m-%dT%H:%M:%SZ")

        return dict