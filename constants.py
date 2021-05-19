from dotenv import dotenv_values

URL_YAHOO = "https://finance.yahoo.com/quote/{scrip_req}/"
URL_NSE = "https://www1.nseindia.com/live_market/dynaContent/live_watch/fomwatchsymbol.jsp"
HEADER_NSE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
RFR = float(0.07)
SCRIP_LOCATION = 'scrips.p'
CONFIRMED_LOCATION = 'confirmed.p'
THRESHOLD = float(2)
RECEIVER_MAIL = 'arvind_gupta@hotmail.com'
AUTH = dotenv_values('.env')
HISTORY_FILENAME = 'completer.hist'
