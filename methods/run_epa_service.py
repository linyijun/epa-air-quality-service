import time
import pandas as pd

from methods.request_data import request_epa_data
from utils.common_db import session
from methods.update_station_info import update_station_name


def one_time_request(start_time, end_time, config):
    """
        Request the EPA data one time, time format 'yyyy-mm-ddThh', e.g., 2019-01-01T04
    """

    options = {'url': 'https://airnowapi.org/aq/data/',
               'start_date': start_time,
               'end_date': end_time,
               'parameters': 'O3,PM25,PM10,CO,NO2,SO2',
               'bbox': config['BOUNDING_BOX'],
               'data_type': 'B',
               'format': 'text/csv',
               'api_key': config['API_KEY']
               }

    res = request_epa_data(options)
    if res['status'] == -1:
        return {'status': -1, 'msg': 'One time request failed.'}

    air_quality_data = res['data']

    # update location name
    new_air_quality_data = update_station_name(air_quality_data, config['EPA_LOC_TABLE'])

    # write data to database
    insert_new_air_quality_data(new_air_quality_data, config['EPA_TABLE'])
    return {'status': 1, 'msg': 'Finish time {}'.format(start_time)}


def multiple_times_request(time_list, config):
    """
        Request the EPA data from time to time, time format 'yyyy-mm-dd hh:00:00', e.g., '2019-03-09 18:00:00'
    """

    def time_to_str(t):
        return str(t).split(' ')[0] + 'T' + str(t).split(' ')[1].split(':')[0]

    for start_time in time_list:
        end_time = start_time + pd.DateOffset(hours=1)

        start_time_str = time_to_str(start_time)
        end_time_str = time_to_str(end_time)

        res = one_time_request(start_time_str, end_time_str, config)
        print(res['msg'])
        time.sleep(30)


def insert_new_air_quality_data(air_quality_data, epa_obj):
    for item in air_quality_data:
        obj = epa_obj(station_id=item['station_id'],
                      date_observed=item['date_observed'],
                      parameter_name=item['parameter_name'],
                      concentration=item['concentration'],
                      unit=item['unit'],
                      aqi=item['aqi'],
                      category_number=item['category_number'])
        session.add(obj)
        session.commit()
