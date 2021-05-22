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

    one_day = timedelta(days=1)
    two_days = timedelta(days=2)
    ninety_six_minutes = timedelta(minutes=96)
    forty_eight_minutes = timedelta(minutes=48)
    seven_and_a_half_hours = timedelta(hours=7.5)
    two_hours = timedelta(hours=2)
    one_hour = timedelta(hours=1)
    four_hours = timedelta(hours=4)
    one_hour_twenty_minutes = timedelta(hours=1, minutes=20)

    DATE_FORMAT = '%Y-%m-%d %H:%M'

    today, tomorrow, day_after_tomorrow = date.today(), date.today() + one_day, date.today() + two_days  # idk, for some reason today, tomorrow, day after tomorrow, reminds me of the song Amar, Akbar, Anthony - may be because it's rhyming, is it?
    print(f'today: {today}; tomorrow: {tomorrow}; day_after_tomorrow: {day_after_tomorrow}')

    # let's create tomorrow's dincharya below #
    routine = []

    # find when to wake up tomorrow
    sunrise = sun(city.observer, date=tomorrow, tzinfo=city.timezone)['sunrise']
    print(f"\ntomorrow's sunrise: {sunrise}")
    wake_up_range = (sunrise - ninety_six_minutes).strftime(DATE_FORMAT), (sunrise - forty_eight_minutes).strftime(
        DATE_FORMAT)    # this period is what is referred as 'Brahmamuhurtha'

    # find when to sleep tomorrow
    day_after_tomorrow_sunrise = sun(city.observer, date=day_after_tomorrow, tzinfo=city.timezone)['sunrise']
    day_after_tomorrow_wake_up_range = day_after_tomorrow_sunrise - ninety_six_minutes, day_after_tomorrow_sunrise - forty_eight_minutes
    sleep_time = day_after_tomorrow_wake_up_range[0] - seven_and_a_half_hours
    routine.append(('sleep_time', sleep_time.strftime(DATE_FORMAT)))

    # based on tomorrow's sleep time, calculate strategic checkpoints for tomorrow, specially "around time-sink" items
    dinner_time = sleep_time - two_hours
    routine.append(('dinner_time', dinner_time.strftime(DATE_FORMAT)))

    evening_recreation_time = dinner_time - one_hour  # well, need to start with something, huh - 1 hour seems decent
    routine.append(('evening_recreation_time', evening_recreation_time.strftime(DATE_FORMAT)))

    resume_work_time = evening_recreation_time - four_hours
    routine.append(('resume_work_time', resume_work_time.strftime(DATE_FORMAT)))

    lunch_time = resume_work_time - one_hour
    routine.append(('lunch_time', lunch_time.strftime(DATE_FORMAT)))

    start_work_time = lunch_time - four_hours
    routine.append(('start_work_time', start_work_time.strftime(DATE_FORMAT)))

    bath_time = start_work_time - one_hour_twenty_minutes  # no no, I am not going to take 1 hour 20 minutes for bath :D; remember, I am just putting checkpoints for strategic items - the slot itself has lot of other items in it to be finished
    routine.append(('bath_time', bath_time.strftime(DATE_FORMAT)))

    routine.append(('wake_up_range', wake_up_range))

    checkpoints_output = f"\ntomorrow's({tomorrow}) checkpoints:\n{tabulate(routine[::-1])}"
    print(checkpoints_output)
    send_telegram(checkpoints_output)

    all_activities = [
        'wake_up',
        'fresh_up',
        'wash_face_and_eyes',
        'brush',
        'physical_activity',
        '*---30 MINS GAP---*',
        'bath',
        'meditate',
        'breakfast',
        '*---30 MINS GAP---*',
        'work',
        'lunch',
        'resume_work',
        'evening_recreation',
        'dinner',
        '*---2 HOURS GAP---*',
        'ratricharya'
    ]
    all_activities_output = f'\nall activities:\n{tabulate(enumerate(all_activities))}'
    print(all_activities_output)
    # send_telegram(all_activities_output)
