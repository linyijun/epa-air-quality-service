import datetime
import pytz
import pandas as pd

from methods.run_epa_service import multiple_times_request, one_time_request
from utils.constants import LOS_ANEGLES


def main(config):

    # From time to time request
    start_time = '2019-04-23 01:00:00'
    end_time = '2019-04-23 03:00:00'

    time_list = pd.date_range(start=start_time, end=end_time, closed='left', freq='1H').tolist()

    multiple_times_request(time_list, config)

    # Current time request
    current_time = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    request_time = str(current_time).split(' ')[0] + 'T' + str(current_time).split(' ')[1].split(':')[0]

    # one_time_request(request_time, request_time, config)


if __name__ == '__main__':
    main(LOS_ANEGLES)
