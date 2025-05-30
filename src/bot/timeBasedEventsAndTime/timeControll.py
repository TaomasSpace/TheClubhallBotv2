import time
import random
import pathlib
import os
import sys
import json
import subprocess

# TODO: add better error handling with Mail if there is an error here what shouldn't happen

BACKUP_FILE = r"backup/backup.json"
COUNTER = "counter"
MONTH = "current_month"
PYTHON3 = "python3"
ROBINHOOD = r"robinHood/robinHood.py"


def daily_reset():
    # set all values from true to false in db(clubhall.db in the Game tab) for claimedDailyGift
    return True


def weekly_reset():
    # set all values from true to false in db(clubhall.db in the Game Section) for claimedWeeklGift
    return True


def shop_reset(): # all months
    # reset Shop items and start acution
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
            subprocess.run([PYTHON3, ROBINHOOD])


def eventsAndSleep():
    now = time.gmtime()
    # time until next midnight in seconds
    time_until_midnight = ((23- now.tm_hour) * 3600 + (59 - now.tm_min) * 60 + (60- now.tm_sec))
    time_until_event = random.randint(0, time_until_midnight - 300) # -300 sec as a buffer if the event is long
    time.sleep(time_until_event)

    which_event() # which event and than starts the event

    now = time.gmtime()
    time_until_midnight_from_now = ((23- now.tm_hour) * 3600 + (59 - now.tm_min) * 60 + (60- now.tm_sec))
    time.sleep(time_until_midnight_from_now)


def initBackupFile(counter_for_reset_weekly, current_month):
    data_to_load = {
        COUNTER: counter_for_reset_weekly,
        MONTH: current_month
    }
    json_object = json.dumps(data_to_load, indent=2)
    with open(BACKUP_FILE, "w") as jsonfile:
        jsonfile.write(json_object)


def updateBackupFile(update_to, update_that):
    with open(BACKUP_FILE, "r") as jsonfile:
        data = json.load(jsonfile)
    
    data[update_that] = update_to

    with open(BACKUP_FILE, "w") as jsonfile:
        json.dump(data, jsonfile, indent=2)


def readValueFromBackupFile(read_that):
    with open(BACKUP_FILE, "r") as jsonfile:
        data = json.load(jsonfile)

    return data[read_that]


def loadValueFromBackupFile(load_that, load_this):
    with open(BACKUP_FILE, "r") as jsonfile:
        data = json.load(jsonfile)

    return data[load_that], data[load_this]


def main(counterForResetWeekly, currentMonth):
    while True:
        daily_reset()
        counterForResetWeekly += 1
        updateBackupFile(counterForResetWeekly, COUNTER)

        if counterForResetWeekly >= 7:
            weekly_reset()
            counterForResetWeekly = 0
            updateBackupFile(counterForResetWeekly, COUNTER)
        
        if readValueFromBackupFile(MONTH) != currentMonth:
            shop_reset()
            updateBackupFile(currentMonth, MONTH)
        
        eventsAndSleep()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        counterForResetWeekly = 0
        now = time.gmtime()
        currentMonth = time.strftime("%m", now)
        initBackupFile(counterForResetWeekly, currentMonth)
        main(counterForResetWeekly, currentMonth)

    else:
        counter, current_month = loadValueFromBackupFile(COUNTER, MONTH)
        main(counter, current_month)