import pytz
import requests
from datetime import datetime


def load_attempts():
    page = 1
    url = 'https://devman.org/api/challenges/solution_attempts/'
    user_info = requests.get(url, params={'page': page}).json()
    while True:
        for record in user_info['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }
        if page == user_info['number_of_pages']:
            break
        page += 1


def get_user_time(user):
    user_timezone = pytz.timezone(user['timezone'])
    user_time = datetime.fromtimestamp(user['timestamp'], user_timezone)
    return user_time


def get_midnighters(users):
    midnight = 0
    sunrise = 7
    midnighters = set()
    for user in users:
        user_time = get_user_time(user)
        if midnight <= user_time.hour <= sunrise:
            midnighters.add(user['username'])
    return midnighters


def show_midnighters(midnighters):
    print('Devman midnighters:')
    for number, midnither in list(enumerate(midnighters, start=1)):
        print('#{}. {}'.format(number, midnither))


if __name__ == '__main__':
    show_midnighters(
        get_midnighters(
            load_attempts()
        ))