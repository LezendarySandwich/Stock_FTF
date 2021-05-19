import os
import readline
import signal
import sys
import threading
from pickle import TRUE
from re import DEBUG
from threading import Thread
from time import sleep, time

from notify import push_notification
from scrape import *
from util.constants import (CONFIRMED_LOCATION, HISTORY_FILENAME,
                            MAIL_CLEAN_SLEEP, MAIL_DELAY, RFR, SCRIP_LOCATION,
                            THRESHOLD, TMP_FILE)
from util.threadsafe_datastructure import ImprovedQueue, threadsafe_set
from util.utility import (HistoryCompleter, color_random, conv_matrix,
                          convert_float, create_csv, excel_list_get, get_fair,
                          log)

os.makedirs(TMP_FILE, exist_ok=True)

if not os.path.exists(SCRIP_LOCATION):
    with open(SCRIP_LOCATION, 'w'):
        pass

if not os.path.exists(CONFIRMED_LOCATION):
    with open(CONFIRMED_LOCATION, 'w'):
        pass

current_scrips = threadsafe_set(SCRIP_LOCATION)
current_print_scrips = threadsafe_set()
current_threads = threadsafe_set()
confirmed_set = threadsafe_set(CONFIRMED_LOCATION)
scrip_mail_set = threadsafe_set()
mail_removal_queue = ImprovedQueue(maxsize=0)  # tuple(scrip, time)


def clean():
    print(log("Cleaning Threads...", state="debug"))
    readline.write_history_file(HISTORY_FILENAME)
    current_scrips.clear()
    for thread in current_threads.items():
        thread.join()


def signal_handler(signal, frame):
    clean()
    raise KeyboardInterrupt


def fair_diff(spot: float, nse_info):
    result = [['Exp date', 'Market', 'Fair', 'Gain', 'Percentage Gain']]
    for row in range(1, 4):
        exp_date = nse_info[row][2]
        fair = get_fair(spot, exp_date)
        market = convert_float(nse_info[row][9])
        if market != "NULL":
            diff = market - fair
            percent = round(diff / spot * 100, 3)
            diff = round(diff, 3)
            market = round(market, 3)
        else:
            diff = "NULL"
            percent = "NULL"
        fair = round(fair, 3)
        result.append([exp_date, market, fair, diff, f'{percent} %'])
    return result


def above_threshold(result):
    for row in range(len(result)):
        if isinstance(result[row][4], float) and result[row][4] >= THRESHOLD.value:
            return True
    return False


def thread_target_scrip(scrip: str):

    print(log(f"{scrip}: Thread started", state="debug"))

    while current_scrips.exist(scrip):

        count_wrong = 0

        for _ in range(3):
            try:
                yahoo_info = get_info(scrip)
                break
            except:
                count_wrong += 1
                sleep(10)

        if count_wrong == 3:
            if confirmed_set.exist(scrip):
                sleep(20)
                continue
            else:
                print(
                    log(f"\n\nIllegal scrip ({scrip}) given (\"Yahoo\")", state="error"))
                remove_scrip(scrip)
                break

        count_wrong = 0

        for _ in range(3):
            try:
                nse_info = get_futures(scrip.split('.')[0])
            except:
                count_wrong += 1
                sleep(10)

        if count_wrong == 3:
            if confirmed_set.exist(scrip):
                sleep(20)
                continue
            else:
                print(
                    log(f"\n\nIllegal scrip ({scrip}) given (\"NSE\")", state='error'))
                remove_scrip(scrip)
                break

        result = fair_diff(convert_float(yahoo_info['spot_price']), nse_info)

        if current_print_scrips.exist(scrip):
            print(
                log(f'\n\nSpot {scrip}: {yahoo_info["spot_price"]}\n', conv_matrix(result) + '\n', state='output'))
            current_print_scrips.remove(scrip)

        if above_threshold(result):
            create_csv(result)
            push_notification(scrip, conv_matrix(result))
            os.remove(os.path.join(
                TMP_FILE, f'{threading.current_thread().name}.csv'))

            mail_removal_queue.put(tuple(scrip, time()))
            scrip_mail_set.insert(scrip)

    print(log(f'{scrip} Thread over', state='debug'))


def add_scrip(scrip):
    current_scrips.insert(scrip)
    scrip_thread = Thread(name=f'{scrip} Thread',
                          target=thread_target_scrip, args=(scrip, ))
    scrip_thread.start()
    current_threads.insert(scrip_thread)


def remove_scrip(scrip):
    current_scrips.remove(scrip)


def thread_command():
    while True:
        cmd = input(log('Enter command (?/help): ')).lower().strip()
        if cmd == "rm":
            scrip = input(log("Enter scrip: "))
            scrip = scrip.upper()
            if not current_scrips.exist(scrip=scrip):
                print(log("Please enter a valid scrip", state='error'))
                continue
            remove_scrip(scrip)
        elif cmd == "add":
            scrip = input(log("Enter scrip: "))
            scrip = scrip.upper()
            confirm = input(log("Are you sure of the given scrip (Y/N): "))
            if current_scrips.exist(scrip):
                print(log("Already scanning the scrip", state='debug'))
            else:
                if confirm.lower == 'y':
                    confirmed_set.insert(scrip)
                add_scrip(scrip)
        elif cmd == "get":
            scrip = input(log("Enter scrip: "))
            scrip = scrip.upper()
            if not current_scrips.exist(scrip):
                print(log(f'{scrip} is not being scanned', state='debug'))
            else:
                current_print_scrips.insert(scrip)
        elif cmd == 'read_xl':
            excel_name = input(
                log("Enter excel name (absolute/relative path): "))
            if not os.path.exists(excel_name):
                print(
                    log(f"Please recheck the sheet: {excel_name}", state='error'))
                continue
            try:
                read_list = excel_list_get(excel_name)
            except Exception as e:
                raise KeyboardInterrupt
            for scrip in read_list:
                confirmed_set.insert(scrip)
                if not current_scrips.exist(scrip):
                    add_scrip(scrip)
                else:
                    print(log(f'{scrip} already running', state='debug'))
        elif cmd == "upd_thresh":
            new_thresh = input(
                log(f"Enter new threshold percentage (Just write number) (Current: {THRESHOLD.value} %): "))
            try:
                THRESHOLD.value = float(new_thresh)
            except:
                print(log("Recheck... it should be a number", state='error'))
        elif cmd == "upd_rfr":
            new_rfr = input(
                log(f"Enter new RFR percentage (Just write number) (Current: {round(RFR.value * 100, 2)} %): "))
            try:
                new_rfr = float(new_rfr)
                RFR.value = new_rfr / 100
            except:
                print(log("Recheck... it should be a number", state='error'))
        elif cmd == "exit":
            clean()
            return
        elif cmd == "list":
            print(log(str(current_scrips.to_list()), state="output"))
        elif cmd == "cls":
            os.system('cls||clear')
        elif cmd == "help" or cmd == "?":
            print(
                log("Commands: rm, add, get, list, read_xl, upd_thresh, upd_rfr, cls, exit", state="output"))
        else:
            print(log("Enter a valid command", state='error'))


def clean_mail_thread_target():
    while True:
        sleep(MAIL_CLEAN_SLEEP)
        count_remove = 0
        current_time = time()
        for scrip, scrip_time in mail_removal_queue.to_list():
            time_diff = current_time - scrip_time
            if time_diff > MAIL_DELAY:
                count_remove += 1
            else:
                break
        for _ in range(count_remove):
            scrip = mail_removal_queue.get_nowait()[0]
            print(log(f'{scrip}: Back to mailing state', state='debug'))


def init_threads():
    for scrip in current_scrips.to_list():
        add_scrip(scrip)


def main():
    init_threads()
    cmd_thread = Thread(name="Command Thread", target=thread_command)
    cmd_thread.start()
    cleaner_mail_thread = Thread(
        name="Mail set cleaner Thread", target=clean_mail_thread_target)
    cleaner_mail_thread.setDaemon(True)
    cleaner_mail_thread.start()
    try:
        cmd_thread.join()
    except KeyboardInterrupt:
        print(log("Exiting...", state='error'))
        print(
            log("Please think of using exit command (next time) :( ...", state='error'))
        os._exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)

    readline.set_completer(HistoryCompleter().complete)
    readline.parse_and_bind('tab: complete')

    if os.path.exists(HISTORY_FILENAME):
        readline.read_history_file(HISTORY_FILENAME)
    else:
        with open(HISTORY_FILENAME, 'w'):
            pass

    print(log(mssg='STOX CLI', color=color_random(), figlet=TRUE))

    main()
