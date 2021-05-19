import os
import signal
import sys
import readline
import threading
from threading import Lock, Thread
from time import sleep

from constants import scrip_location, threshold, HISTORY_FILENAME
from notify import push_notification
from scrape import *
from threadsafe_set import threadsafe_set
from utility import conv_matrix, convert_float, create_csv, get_fair, HistoryCompleter

if not os.path.exists(scrip_location):
    with open(scrip_location, 'w'):
        pass

os.makedirs('.tmp', exist_ok=True)

current_scrips = threadsafe_set(scrip_location)
current_print_scrips = threadsafe_set()
current_threads = threadsafe_set()


def clean():
    print("Cleaning Threads...")
    readline.write_history_file(HISTORY_FILENAME)
    current_scrips.clear()
    for thread in current_threads.items():
        thread.join()


def signal_handler(signal, frame):
    clean()
    sys.exit(0)


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
        if isinstance(result[row][4], float) and result[row][4] >= threshold:
            return True
    return False


def thread_target_scrip(scrip: str):
    while current_scrips.exist(scrip):

        count_wrong = 0

        for _ in range(3):
            try:
                yahoo_info = get_info(scrip)
                break
            except:
                count_wrong += 1

        if count_wrong == 3:
            print(f"\n\nIllegal scrip ({scrip}) given (\"Yahoo\")")
            remove_scrip(scrip)
            break

        count_wrong = 0

        for _ in range(3):
            try:
                nse_info = get_futures(scrip.split('.')[0])
            except:
                count_wrong += 1

        if count_wrong == 3:
            print(f"\n\nIllegal scrip ({scrip}) given (\"NSE\")")
            remove_scrip(scrip)
            break

        result = fair_diff(convert_float(yahoo_info['spot_price']), nse_info)

        if current_print_scrips.exist(scrip):
            print(
                f'\n\nSpot {scrip}: {yahoo_info["spot_price"]}\n', conv_matrix(result) + '\n')
            current_print_scrips.remove(scrip)

        if above_threshold(result):
            create_csv(result)
            push_notification(scrip, conv_matrix(result))
            os.remove(os.path.join(
                '.tmp', f'{threading.current_thread().name}.csv'))
            sleep(15 * 60)
    print(f'{scrip} Thread over')


def add_scrip(scrip):
    scrip_thread = Thread(name=f'{scrip} Thread',
                          target=thread_target_scrip, args=(scrip, ))
    scrip_thread.start()
    current_threads.insert(scrip_thread)


def remove_scrip(scrip):
    current_scrips.remove(scrip)


def thread_command():
    while True:
        cmd = input('Enter command (rm, add, get, list, cls, exit): ')
        readline.insert_text('fdnslkdfnl')
        readline.redisplay()
        cmd = cmd.lower()
        if cmd == "rm":
            scrip = input("Enter scrip: ")
            if not current_scrips.exist(scrip=scrip):
                print("Please enter a valid scrip")
                continue
            remove_scrip(scrip)
        elif cmd == "add":
            scrip = input("Enter scrip: ")
            if current_scrips.exist(scrip):
                print("Already scanning the scrip")
            else:
                current_scrips.insert(scrip)
                add_scrip(scrip)
        elif cmd == "get":
            scrip = input("Enter scrip: ")
            if not current_scrips.exist(scrip):
                print(f'{scrip} is not being scanned')
            else:
                current_print_scrips.insert(scrip)
        elif cmd == "exit":
            clean()
            return
        elif cmd == "list":
            for scrip in current_scrips.items():
                print(scrip, end=', ')
            print()
        elif cmd == "cls":
            os.system('cls||clear')
        else:
            print("Enter a valid command")


def init_threads():
    for scrip in current_scrips.items():
        add_scrip(scrip)


def main():
    init_threads()
    cmd_thread = Thread(name="Command Thread", target=thread_command)
    cmd_thread.setDaemon(True)
    cmd_thread.start()
    if current_scrips.empty():
        print("No running scrips. Exiting in 30 seconds if none provided")
        sleep(30)


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

    main()