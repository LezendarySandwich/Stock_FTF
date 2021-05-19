from dotenv import dotenv_values

url_yahoo = "https://finance.yahoo.com/quote/{scrip_req}/"
url_nse = "https://www1.nseindia.com/live_market/dynaContent/live_watch/fomwatchsymbol.jsp"
header_nse = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
RFR = float(0.07)
scrip_location = 'scrips.p'
threshold = float(2)
receiver_mail = 'arvind_gupta@hotmail.com'
auth = dotenv_values('.env')
HISTORY_FILENAME = 'completer.hist'
