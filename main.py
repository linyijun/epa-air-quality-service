import datetime
import pytz

from methods.run_epa_service import time_to_time_request, one_time_request


def main():

    # From time to time request
    start_time = '2019-04-22 23:00:00'
    end_time = '2019-04-23 02:00:00'
    time_to_time_request(start_time, end_time)

    # Current time request
    current_time = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    request_time = str(current_time).split(' ')[0] + 'T' + str(current_time).split(' ')[1].split(':')[0]

    # one_time_request(request_time, request_time)


if __name__ == '__main__':
    main()
