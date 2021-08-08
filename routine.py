import json
import os

import requests
from astral import LocationInfo
from datetime import date, timedelta
from astral.sun import sun
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
LOCATION = (json.loads(os.environ['LOCATION']))


def send_telegram(message):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage" \
          f"?chat_id={os.environ['TELEGRAM_BOT_CHAT_ID']}&parse_mode=HTML&text=<pre>{message}</pre>"
    requests.post(url)


if __name__ == '__main__':
    city = LocationInfo(*LOCATION)

    thirty_minutes = timedelta(minutes=30)
    one_hour = timedelta(hours=1)
    ninety_six_minutes = timedelta(minutes=96)
    two_hours = timedelta(hours=2)
    two_and_a_half_hours = timedelta(hours=2.5)
    four_hours = timedelta(hours=4)
    six_hours = timedelta(hours=6)
    one_day = timedelta(days=1)
    two_days = timedelta(days=2)

    tomorrow, day_after_tomorrow = date.today() + one_day, date.today() + two_days

    sun_tomorrow = sun(city.observer, date=tomorrow, tzinfo=city.timezone)
    sunrise, sunset = sun_tomorrow['sunrise'], sun_tomorrow['sunset']   # Eating window

    # let's create tomorrow's routine below #
    routine = []
    DATE_FORMAT = '%Y-%m-%d %H:%M'
    
    wake_up_time = sunrise - ninety_six_minutes    # Start of Brahmamuhurtha. Any Muhurtha is 48 mins long.
    routine.append(('wake_up_time', wake_up_time.strftime(DATE_FORMAT)))
    
    # self: yoga-abhyas, pranayam, dhyaan etc. -> 2 hours
    self_time_range = (wake_up_time + thirty_minutes).strftime(DATE_FORMAT), (wake_up_time + two_and_a_half_hours).strftime(DATE_FORMAT)
    routine.append(('self_time_range', self_time_range))

    # food
    breakfast_time, lunch_time, dinner_time = sunrise + one_hour, sun_tomorrow['noon'], sunset - thirty_minutes
    routine.append(('breakfast_time', breakfast_time.strftime(DATE_FORMAT)))    # this is the minimum time, can eat anytime post this
    routine.append(('lunch_time', lunch_time.strftime(DATE_FORMAT)))

    # family -> 2 hours
    family_time_range = (dinner_time - two_hours).strftime(DATE_FORMAT), dinner_time.strftime(DATE_FORMAT)
    routine.append(('family_time_range', family_time_range))

    routine.append(('dinner_time', dinner_time.strftime(DATE_FORMAT)))
    
    # sleep (includes sex) -> 6 hours
    day_after_tomorrow_sunrise = sun(city.observer, date=day_after_tomorrow, tzinfo=city.timezone)['sunrise']
    day_after_tomorrow_wake_up_time = day_after_tomorrow_sunrise - ninety_six_minutes   # Start of Brahmamuhurtha. Any Muhurtha is 48 mins long.
    sleep_time_range = (day_after_tomorrow_wake_up_time - six_hours).strftime(DATE_FORMAT), (day_after_tomorrow_wake_up_time).strftime(DATE_FORMAT)
    routine.append(('sleep_time_range', sleep_time_range))

    # work -> 14 hours (basically, everything else from above is work)

    routine_output = f"\ntomorrow's({tomorrow}) routine:\n{tabulate(routine)}"
    print(routine_output)
    # send_telegram(checkpoints_output)
