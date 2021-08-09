import json
import os

import requests
from astral import LocationInfo
from datetime import date, timedelta
from astral.sun import sun
from dotenv import load_dotenv
from tabulate import tabulate
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()
LOCATION = (json.loads(os.environ['LOCATION']))
CALENDAR_ID = os.environ.get('CALENDAR_ID', 'primary')
SCOPES = ['https://www.googleapis.com/auth/calendar']  # If modifying these scopes, delete the file token.json.


def format_message(routine):
    table = [(event, tuple((t.strftime('%d %b %Y %H:%M') for t in time_range))) for event, time_range in routine]
    return f"\n{tomorrow.strftime('%d %b %Y')} routine:\n{tabulate(table)}"


def send_telegram(routine):
    telegram_message = format_message(routine)
    print(f'telegram_message:\n{telegram_message}')
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage" \
          f"?chat_id={os.environ['TELEGRAM_BOT_CHAT_ID']}&parse_mode=HTML&text=<pre>{telegram_message}</pre>"
    requests.post(url)


def get_calendar_resource():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def create_calendar_events(events_info):
    service = get_calendar_resource()

    for event_info in events_info:
        name, start, end = event_info[0], event_info[1][0], event_info[1][0] if len(event_info[1]) < 2 else event_info[1][1]
        start, end = start.isoformat(), end.isoformat()
        print(f'{name=} {start=} {end=}')

        event = {
            'summary': name,
            'start': {
                'dateTime': start
            },
            'end': {
                'dateTime': end
            }
        }

        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

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
    
    wake_up_time = sunrise - ninety_six_minutes    # Start of Brahmamuhurtha. Any Muhurtha is 48 mins long.
    routine.append(('wake_up_time', (wake_up_time,)))
    
    # self: yoga-abhyas, pranayam, dhyaan etc. -> 2 hours
    self_time_range = wake_up_time + thirty_minutes, wake_up_time + two_and_a_half_hours
    routine.append(('self_time_range', self_time_range))

    # food
    breakfast_time, lunch_time, dinner_time = sunrise + one_hour, sun_tomorrow['noon'], sunset - thirty_minutes
    routine.append(('breakfast_time', (breakfast_time,)))    # this is the minimum time, can eat anytime post this
    routine.append(('lunch_time', (lunch_time,)))

    # family -> 2 hours
    family_time_range = dinner_time - two_hours, dinner_time
    routine.append(('family_time_range', family_time_range))

    routine.append(('dinner_time', (dinner_time,)))
    
    # sleep (includes sex) -> 6 hours
    day_after_tomorrow_sunrise = sun(city.observer, date=day_after_tomorrow, tzinfo=city.timezone)['sunrise']
    day_after_tomorrow_wake_up_time = day_after_tomorrow_sunrise - ninety_six_minutes   # Start of Brahmamuhurtha. Any Muhurtha is 48 mins long.
    sleep_time_range = day_after_tomorrow_wake_up_time - six_hours, day_after_tomorrow_wake_up_time
    routine.append(('sleep_time_range', sleep_time_range))

    # work -> 14 hours (basically, everything else from above is work)

    send_telegram(routine)
    create_calendar_events(routine)

    # TODO: update the cron to daily 2 AM
