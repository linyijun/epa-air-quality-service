from utils.common_db import session


def update_station_name(air_quality_data, loc_obj):

    air_quality_data_res = []
    stations, max_station_id = find_station_info(loc_obj)
    for item in air_quality_data:
        station_id = stations.get((item['lon'], item['lat']))
        if station_id:
            item['station_id'] = station_id
        else:
            new_station_id = max_station_id + 1
            item['station_id'] = new_station_id
            insert_new_station_id(new_station_id, item['lon'], item['lat'], loc_obj)

        air_quality_data_res.append(item)
    return air_quality_data_res


def insert_new_station_id(new_station_id, lon, lat, loc_obj):

    point = 'POINT({} {})'.format(lon, lat)
    obj = loc_obj(station_id=new_station_id, lon=lon, lat=lat, location=point)
    session.add(obj)
    session.commit()


def find_station_info(loc_obj):

    search_results = session.query(loc_obj)\
        .with_entities(*[loc_obj.station_id, loc_obj.lon, loc_obj.lat]).all()

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
