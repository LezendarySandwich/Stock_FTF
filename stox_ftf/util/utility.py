import csv
import datetime
import os
import random
from re import DEBUG
import readline
import threading
from collections import Counter
from math import exp

import openpyxl as xl
from prettytable import PrettyTable
from pyfiglet import Figlet
from termcolor import colored

from .constants import (DEBUG_COLOR, ERROR_COLOR, FIGLET_FONT, LIST_COLOR, PRIORITY_COLOR, RFR,
                        TMP_FILE)

fig_conv = Figlet(font=FIGLET_FONT)


def color_random():
    return random.choice(LIST_COLOR)


cmd_col = color_random()
out_col = color_random()
while out_col == cmd_col:
    out_col = color_random()


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
    return spot * exp(RFR.value * diff / 365)


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
    path_csv = os.path.join(TMP_FILE, f'{name_thread}.csv')
    with open(path_csv, "w") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(matrix)


def get_history_items():
    num_items = readline.get_current_history_length() + 1
    return [
        readline.get_history_item(i)
        for i in range(1, num_items)
    ]


def excel_list_get(file_name: str):
    wb = xl.load_workbook(filename=file_name)
    if len(wb.get_sheet_names()) == 1:
        sheet = wb.get_sheet_by_name(wb.get_sheet_names()[0])
    else:
        sheet_name = input("Enter sheet name: ")
        sheet = wb.get_sheet_by_name(sheet_name)
    column = input("Enter column name: ")
    ret_list = list()
    for row in range(2, sheet.max_row + 1):
        cell_name = f'{column}{row}'
        cell_val = sheet[cell_name].value
        if cell_val:
            ret_list.append(cell_val.upper())
    return ret_list


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


def log(mssg: str, color: str = cmd_col, figlet=False, state='cmd'):
    if figlet:
        mssg = fig_conv.renderText(mssg)
        text = colored(mssg, color, attrs=['dark', 'bold'])
        return text
    elif state == 'cmd':
        return colored(mssg, color)
    elif state == 'error':
        return colored(mssg, ERROR_COLOR)
    elif state == 'debug':
        return colored(mssg, DEBUG_COLOR, attrs=['dark'])
    elif state == 'output':
        return colored(mssg, out_col, attrs=['bold'])
    elif state == 'priority':
        return colored(mssg, PRIORITY_COLOR, attrs=['blink'])
    else:
        return mssg
