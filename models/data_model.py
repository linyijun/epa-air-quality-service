from sqlalchemy import Column, BigInteger, Integer, String, Float, DateTime, Text, REAL, Sequence
from geoalchemy2 import Geometry

from models.common_db import Base


class LosAngelesEpa(Base):
    __tablename__='los_angeles_epa_air_quality_2019'
    __table_args__ = {'schema' : 'air_quality_data'}

    uid_seq = Sequence('los_angeles_epa_air_quality_2019_uid_seq')
    uid = Column(BigInteger, primary_key=True, nullable=False,
                 server_default=uid_seq.next_value())
    station_id = Column(Integer, nullable=False)
    date_observed = Column(DateTime, nullable=False)
    parameter_name = Column(String(10), nullable=False)
    concentration = Column(REAL, nullable=False)
    unit = Column(Text)
    aqi = Column(REAL,  nullable=False)
    category_number = Column(Integer)


class LosAngelesEpaLocation(Base):
    __tablename__='los_angeles_epa_sensor_locations'
    __table_args__ = {'schema' : 'air_quality_data'}

    station_id = Column(BigInteger, nullable=False, primary_key=True)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    elevation = Column(Float(53), nullable=False)
