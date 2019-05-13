import time
import pandas as pd

from methods.request_data import request_epa_data
from models.data_model import LosAngelesEpa
from models.common_db import session
from methods.update_station_info import update_station_name


def one_time_request(start_time, end_time):
    """
        Request the EPA data one time, time format 'yyyy-mm-ddThh', e.g., 2019-01-01T04
    """

    options = {'url': 'https://airnowapi.org/aq/data/',
               'start_date': start_time,
               'end_date': end_time,
               'parameters': 'O3,PM25,PM10,CO,NO2,SO2',
               'bbox': '-119.017,33.704,-117.591,34.638',
               'data_type': 'B',
               'format': 'text/csv',
               'api_key': '0614E979-0022-41A8-8FEF-3575B04F4332'
               }

    air_quality_data = request_epa_data(options)
    if air_quality_data is None or len(air_quality_data) == 0:
        return 0

    # update location name
    new_air_quality_data = update_station_name(air_quality_data)

    # write data to database
    insert_new_air_quality_data(new_air_quality_data)
    return 1


def time_to_time_request(start_time, end_time):
    """
        Request the EPA data from time to time, time format 'yyyy-mm-dd hh:00:00', e.g., '2019-03-09 18:00:00'
    """

    start_list = pd.date_range(start=start_time, end=end_time, freq='1H').tolist()
    end_list = [x + pd.DateOffset(hours=1) for x in start_list]
    start_list = [str(x).split(' ')[0] + 'T' + str(x).split(' ')[1].split(':')[0] for x in start_list]
    end_list = [str(x).split(' ')[0] + 'T' + str(x).split(' ')[1].split(':')[0] for x in end_list]

    for i in range(len(start_list)):
        r = one_time_request(start_list[i], end_list[i])
        if r:
            print(start_list[i])
            time.sleep(30)
    return 1


def insert_new_air_quality_data(air_quality_data):
    for item in air_quality_data:
        obj = LosAngelesEpa(station_id=item['station_id'],
                            date_observed=item['date_observed'],
                            parameter_name=item['parameter_name'],
                            concentration=item['concentration'],
                            unit=item['unit'],
                            aqi=item['aqi'],
                            category_number=item['category_number'])
        session.add(obj)
        session.commit()

# def get_request_time(table_name, time_column_name, conn):
#
#     max_time = get_max_time(table_name, time_column_name, conn)
#     start_time = max_time + timedelta(hours=1)
#     tz = pytz.utc
#     end_time = datetime.now(tz)
#
#     if start_time >= end_time:
#         return None, None
#
#     start_time_str = str(start_time).split(' ')[0] + 'T' + str(start_time).split(' ')[1].split(':')[0]
#     end_time_str = str(end_time).split(' ')[0] + 'T' + str(end_time).split(' ')[1].split(':')[0]
#     return start_time_str, end_time_str
