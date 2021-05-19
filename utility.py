import csv
import datetime
import os
import readline
import threading
from math import exp

from prettytable import PrettyTable

from constants import RFR
from collections import Counter


def get_month_number(month: str):
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = datetime_object.month
    return month_number


def get_diff_days(day: str):
    year = int(day[-4:])
    month = get_month_number(day[-7:-4])
    day = int(day[:-7])
    d1 = datetime.datetime(year, month, day)
    d2 = datetime.datetime.today()
    return float(abs((d2 - d1).days))


def get_fair(spot: float, day: str):
    diff = get_diff_days(day)
    return spot * exp(RFR * diff / 365)


def conv_matrix(mat):
    matrix = PrettyTable()
    matrix.field_names = mat[0]
    for row in range(1, len(mat)):
        new_row = list()
        for val in mat[row]:
            if isinstance(val, float):
                new_row.append(round(val, 3))
            else:
                new_row.append(val)
        matrix.add_row(new_row)
    return str(matrix)


def convert_float(value: str):
    try:
        return float(value.replace(',', ''))
    except:
        return 'NULL'


def create_csv(matrix):
    name_thread = threading.current_thread().name
    path_csv = os.path.join('.tmp', f'{name_thread}.csv')
    with open(path_csv, "w") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(matrix)


def get_history_items():
    num_items = readline.get_current_history_length() + 1
    return [
        readline.get_history_item(i)
        for i in range(1, num_items)
    ]


class HistoryCompleter:

    def __init__(self):
        self.matches = []

    def complete(self, text, state):
        response = None
        if state == 0:
            history_values = get_history_items()
            history_dict = Counter(history_values)
            if text:
                self.matches = [
                    h
                    for h in history_values
                    if h and h.startswith(text)
                ]
                self.matches.sort(reverse=True, key=lambda x: history_dict[x])
            else:
                self.matches = []
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response
