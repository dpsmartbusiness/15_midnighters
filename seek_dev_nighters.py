import pytz
import requests
from datetime import datetime


def load_attempts():
    page_num = 1
    url = 'https://devman.org/api/challenges/solution_attempts/'
    while True:
        page = requests.get(url, params={'page': page_num}).json()
        attempts = page['records']
        for attempt in attempts:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }
        if page_num == page['number_of_pages']:
            break
        page_num += 1


def get_attempt_time(attempt):
    attempt_timezone = pytz.timezone(attempt['timezone'])
    attempt_time = datetime.fromtimestamp(
        attempt['timestamp'],
        attempt_timezone
    )
    return attempt_time


def get_midnighters(attempts_generator):
    midnight = 0
    sunrise = 7
    midnighters = set()
    for attempt in attempts_generator:
        attempt_time = get_attempt_time(attempt)
        if midnight <= attempt_time.hour <= sunrise:
            midnighters.add(attempt['username'])
    return midnighters


def show_midnighters(midnighters):
    print('Devman midnighters:')
    for number, midnighter in list(enumerate(midnighters, start=1)):
        print('#{}. {}'.format(number, midnighter))


if __name__ == '__main__':
    show_midnighters(
        get_midnighters(
            load_attempts()
        ))