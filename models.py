from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ConsumptionRecord(Base):
    __tablename__ = 'consumption'

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(String)
    country = Column(String)
    urbanisation = Column(String)
    coicop = Column(String)
    year = Column(Integer)
    value = Column(Float)
