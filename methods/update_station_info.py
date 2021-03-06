from data_models.common_db import session
from data_models.epa_model import LosAngelesEPALocation


def update_station_name(air_quality_data):

    air_quality_data_res = []
    stations, max_station_id = find_station_info()
    for item in air_quality_data:
        station_id = stations.get((item['lon'], item['lat']))
        if station_id is not None:
            item['station_id'] = station_id
        else:
            item['station_id'] = max_station_id + 1
            stations[(item['lon'], item['lat'])] = item['station_id']
            insert_new_station_id(item['station_id'], item['lon'], item['lat'])
            max_station_id += 1

        air_quality_data_res.append(item)
    return air_quality_data_res


def insert_new_station_id(new_station_id, lon, lat):

    point = 'SRID=4326;POINT({} {})'.format(lon, lat)
    obj = LosAngelesEPALocation(station_id=new_station_id, lon=lon, lat=lat, location=point, elevation=0.0)
    session.add(obj)
    session.commit()


def find_station_info():

    search_results = session.query(LosAngelesEPALocation)\
        .with_entities(*[LosAngelesEPALocation.station_id, LosAngelesEPALocation.lon, LosAngelesEPALocation.lat]).all()

    if not search_results:
        return None
    else:
        station_dict = {}
        max_station_id = 0
        for res in search_results:
            station_dict[(res.lon, res.lat)] = res.station_id
            if res.station_id > max_station_id:
                max_station_id = res.station_id
        return station_dict, max_station_id
