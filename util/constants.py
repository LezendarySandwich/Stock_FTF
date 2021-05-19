import os

from dotenv import dotenv_values

from util.threadsafe_datastructure import AtomicFloat

from .threadsafe_datastructure import AtomicFloat

cwd = os.getcwd()

# URI
URL_YAHOO = "https://finance.yahoo.com/quote/{scrip_req}/"
URL_NSE = "https://www1.nseindia.com/live_market/dynaContent/live_watch/fomwatchsymbol.jsp"
HEADER_NSE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

# FILE LOCATIONS
TMP_FILE = os.path.join(cwd, 'util', '.tmp')
HISTORY_FILENAME = os.path.join(TMP_FILE, 'completer.hist')
SCRIP_LOCATION = os.path.join(TMP_FILE, 'scrips.p')
CONFIRMED_LOCATION = os.path.join(TMP_FILE, 'confirmed.p')
THRESH_LOCATION = os.path.join(TMP_FILE, '.thresh')
RFR_LOCATION = os.path.join(TMP_FILE, '.rfr')

# USER-THRESHOLDS
RFR_INIT = float(0.07)
THRESHOLD_INIT = float(2)

# ATOMIC CLASS
THRESHOLD = AtomicFloat(THRESH_LOCATION, THRESHOLD_INIT)
RFR = AtomicFloat(RFR_LOCATION, RFR_INIT)

# MAIL
RECEIVER_MAIL = 'arvind_gupta@hotmail.com'
AUTH = dotenv_values('.env')


# DELAY
MAIL_DELAY = int(15 * 60)
MAIL_CLEAN_SLEEP = int(10 * 60)
