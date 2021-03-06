import os

from dotenv import dotenv_values

from .threadsafe_datastructure import AtomicFloat

from .threadsafe_datastructure import AtomicFloat
from pathlib import Path

cwd = Path(__file__).parent.absolute()

# URI
URL_YAHOO = "https://finance.yahoo.com/quote/{scrip_req}/"
URL_NSE = "https://www1.nseindia.com/live_market/dynaContent/live_watch/fomwatchsymbol.jsp"
HEADER_NSE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
HEADER_YAHOO = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close'}

# FILE LOCATIONS
TMP_FILE = os.path.join(cwd, '.tmp')
os.makedirs(TMP_FILE, exist_ok=True)
HISTORY_FILENAME = os.path.join(TMP_FILE, 'completer.hist')
SCRIP_LOCATION = os.path.join(TMP_FILE, 'scrips.p')
CONFIRMED_LOCATION = os.path.join(TMP_FILE, 'confirmed.p')
THRESH_LOCATION = os.path.join(TMP_FILE, '.thresh')
RFR_LOCATION = os.path.join(TMP_FILE, '.rfr')
DRIVER_PATH = os.path.join(cwd, '..', '..', 'drivers')
FIREFOX_DRIVER = os.path.join(DRIVER_PATH, 'geckodriver')
FIREFOX_LOG = os.path.join(TMP_FILE, 'geckodriver.log')

# USER-THRESHOLDS
RFR_INIT = float(0.07)
THRESHOLD_INIT = float(2)

# ATOMIC CLASS
THRESHOLD = AtomicFloat(THRESH_LOCATION, THRESHOLD_INIT)
RFR = AtomicFloat(RFR_LOCATION, RFR_INIT)

# MAIL
AUTH = dotenv_values(os.path.join(cwd, '..', '..', '.env'))
RECEIVER_MAIL = AUTH['receive_email']

# DELAY
MAIL_DELAY = int(15 * 60)
MAIL_CLEAN_SLEEP = int(10 * 60)

# BEAUTIFY
LIST_COLOR = ['green', 'yellow', 'cyan']
FIGLET_FONT = 'standard'
ERROR_COLOR = 'red'
DEBUG_COLOR = 'white'
PRIORITY_COLOR = 'magenta'
