import time
import random
from pathlib import Path
import sys
import json
import subprocess
import configparser

# TODO: add better error handling with Mail if there is an error here what shouldn't happen

CONFIG_PATH = Path(r"../config.ini")
config = configparser.ConfigParser()
config.optionxform = str # not so important only if you use array/lists
if CONFIG_PATH.is_file() and CONFIG_PATH.exists():
    config.read(CONFIG_PATH)


def daily_reset():
    # set all values from true to false in db(clubhall.db in the Game tab) for claimedDailyGift
    return True


def weekly_reset():
    # set all values from true to false in db(clubhall.db in the Game Section) for claimedWeeklyGift
    return True


def shop_reset(): # all months
    # reset Shop items and start auction
    return True


def which_event():
    """
    Start a random event

    Returns:
    -True
    """
    num = random.randint(1, 1) # TODO: when there are more events it gets updated
    match num:
        case 1:
            subprocess.run([config['SystemData']['python'], config['Events']['robinhood']])


def events_and_sleep():
    now = time.gmtime()
    # time until next midnight in seconds
    time_until_midnight = ((23- now.tm_hour) * 3600 + (59 - now.tm_min) * 60 + (60- now.tm_sec))
    time_until_event = random.randint(0, time_until_midnight - 300) # -300 sec as a buffer if the event is long
    time.sleep(time_until_event)

    which_event() # which event and then starts the event

    now = time.gmtime()
    time_until_midnight_from_now = ((23- now.tm_hour) * 3600 + (59 - now.tm_min) * 60 + (60- now.tm_sec))
    time.sleep(time_until_midnight_from_now)


def init_backup_file(counter_for_reset_weekly_temp, current_month_temp):

    data_to_load = {
        config['RandomTimeBasedStuff']['counter']: counter_for_reset_weekly_temp,
        config['RandomTimeBasedStuff']['month']: current_month_temp
    }

    json_object = json.dumps(data_to_load, indent=2)
    with open(config['Backup']['backup_file'], "w") as jsonfile:
        jsonfile.write(json_object)


def update_backup_file(update_to, update_that):
    with open(config['Backup']['backup_file'], "r") as jsonfile:
        data = json.load(jsonfile)
    
    data[update_that] = update_to

    with open(config['Backup']['backup_file'], "w") as jsonfile:
        json.dump(data, jsonfile, indent=2)


def read_value_from_backup_file(read_that):
    with open(config['Backup']['backup_file'], "r") as jsonfile:
        data = json.load(jsonfile)

    return data[read_that]


def load_value_from_backup_file(load_that, load_this):
    with open(config['Backup']['backup_file'], "r") as jsonfile:
        data = json.load(jsonfile)

    return data[load_that], data[load_this]


def main(counter_for_reset_weekly_main, current_month_main):
    while True:
        daily_reset()
        counter_for_reset_weekly_main += 1
        update_backup_file(counter_for_reset_weekly_main, config['RandomTimeBasedStuff']['counter'])

        if counter_for_reset_weekly_main >= 7:
            weekly_reset()
            counter_for_reset_weekly_main = 0
            update_backup_file(counter_for_reset_weekly_main, config['RandomTimeBasedStuff']['counter'])
        
        if read_value_from_backup_file(config['RandomTimeBasedStuff']['month']) != current_month_main:
            shop_reset()
            update_backup_file(current_month_main, config['RandomTimeBasedStuff']['month'])
        
        events_and_sleep()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        counter_for_reset_weekly_init = 0
        now_init = time.gmtime()
        current_month_init = time.strftime("%m", now_init)
        init_backup_file(counter_for_reset_weekly_init, current_month_init)
        main(counter_for_reset_weekly_init, current_month_init)

    else:
        counter, current_month = load_value_from_backup_file(config['RandomTimeBasedStuff']['counter'], config['RandomTimeBasedStuff']['month'])
        main(counter, current_month)