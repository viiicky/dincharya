# dincharya

This script sends you a daily routine designed around sunrise and sunset timings of your location!

Inspired from https://youtu.be/6ZUFT0CwU1w, https://youtu.be/0vGWYrIpoII and https://www.notion.so/Dincharya-Lifestyle-Life-management-by-Swami-Ramdev-c068630599114c9db7202ebe29f40322

## Steps
1. Since this script sends a message to Telegram using a Telegram bot, you need to set Telegram specific tokens in your environment variables. Create your Telegram bot and then:

    `export TELEGRAM_BOT_TOKEN=<your telegram bot token>`
  
    `export TELEGRAM_BOT_CHAT_ID=<the id of the chat where you want this message to appear>`
  
2. You also need to set the location env. An example location value could be:

    `export LOCATION='["Morar","Gwalior","Asia/Kolkata",26.24074743965471,78.22283739759605]'`
  
    Here `Asia/Kolkata` represents the timezone, so it must be a valid input. List of timezones can be obtained from `pytz.all_timezones`
  
    The last two values are latitude, longitude.
  
    The first two values represent name and region respectively, and can be anything.

3. For events to be created on the Google Calendar:
    
    You need to have `credentials.json` in the root of this project. You can create a Desktop application credentials by referring to https://developers.google.com/workspace/guides/create-credentials

    Also `export CALENDAR_ID={your-email-here}` to set the destination calendar. If not set, it will use the primary calendar of the logged in user.
  
4. Set up virtual env

    `cd <root of this repo>`
  
    `python3 -m venv <virtual-env-name>`
  
    `pip install -r requirements.txt`

5. Run

    `source <virtual-env-name>/bin/activate`
    
    `python routine.py`

You can also put this script as a cronjob to send you daily routines. An example of that can be:

`0 2 * * * ~/dincharya/dincharya-env/bin/python ~/dincharya/routine.py >> ~/logs/dincharya/routine.out`
