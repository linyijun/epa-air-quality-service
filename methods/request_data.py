import requests
from datetime import datetime
import pytz


def request_epa_data(options):

    url = '{url}?parameters={parameters}&bbox={bbox}&datatype={datatype}&format={format}&api_key={api_key}'\
        .format(url=options['url'], parameters=options['parameters'], bbox=options['bbox'],
                datatype=options['data_type'], format=options['format'], api_key=options['api_key'])

    if options.get('start_date') and options.get('end_date'):
        url = '{url}?startDate={start_date}&endDate={end_date}&parameters={parameters}&BBOX={bbox}' \
              '&dataType={datatype}&format={format}&API_KEY={api_key}' \
              .format(url=options['url'], start_date=options['start_date'], end_date=options['end_date'],
                      parameters=options['parameters'], bbox=options['bbox'], datatype=options['data_type'],
                      format=options['format'], api_key=options['api_key'])

    air_quality_data = []
    try:
        raw_data = requests.get(url)
        if raw_data.text == '' or raw_data is None:  # no data
            return {'status': -1, 'msg': 'No data.', 'data': air_quality_data}

        for line in raw_data.text.split('\n'):
            # e.g., line = '"34.21","-118.8694","2018-06-14T16:00","PM2.5","20.3","UG/M3","68","2"'
            if line == '' or line is None:   # no data
                continue

            epa_data = parse_epa_data(line)
            air_quality_data.append(epa_data)
        return {'status': 1, 'msg': '', 'data': air_quality_data}

    except Exception as e:
        print('Request EPA API. Error message: {msg}.'.format(msg=e))
        return {'status': -1, 'msg': 'Request EPA API Failed: {}'.format(e), 'data': air_quality_data}


def parse_epa_data(input_str):

    data = input_str.replace('"', '')
    data_list = data.split(',')

    def get_timestamp(t):
        tz = pytz.timezone('UTC')
        t = datetime.strptime(t, '%Y-%m-%dT%H:%M')
        return tz.localize(t)

    data_dict = {}
    data_dict['lat'] = float(data_list[0])
    data_dict['lon'] = float(data_list[1])

    data_dict['date_observed'] = get_timestamp(data_list[2])
    data_dict['parameter_name'] = data_list[3]
    data_dict['concentration'] = float(data_list[4])
    data_dict['unit'] = data_list[5]
    data_dict['aqi'] = float(data_list[6])
    data_dict['category_number'] = int(data_list[7])
    return data_dict
