import requests
from bs4 import BeautifulSoup
from threading import local
from constants import *

thread_local = local()


def get_session(session):
    if not hasattr(thread_local, session):
        setattr(thread_local, session, requests.Session())
    return getattr(thread_local, session)


def get_info(scrip: str):
    session = get_session("yahoo")
    doc = session.get(url_yahoo.format(scrip_req=scrip))
    soup = BeautifulSoup(doc.text, 'html.parser')
    res_dic = dict()
    soup = soup.body
    spot_tag = soup.find("span", {"data-reactid": "32"})
    res_dic["spot_price"] = spot_tag.text
    soup = soup.find("div", {"id": "quote-summary"})
    for i in range(3):
        soup = soup.contents[0]
    for child_tags in soup.contents:
        res = list()
        for children in child_tags.contents:
            try:
                res.append(children.contents[0].text)
            except:
                pass
        if len(res) == 2:
            res_dic[res[0]] = res[1]
    return res_dic


def get_futures(scrip: str):
    session = get_session("NSE")
    doc = session.get(url_nse, headers=header_nse, params={
        "key": scrip, "Fut_Opt": "Futures"})
    soup = BeautifulSoup(doc.text, 'html.parser')
    soup = soup.find("div", {"id": "tab26Content"}).contents[1]
    result = list()
    for child_tags in soup.contents:
        if not hasattr(child_tags, 'contents'):
            continue
        res = list()
        for children in child_tags.contents:
            try:
                res.append(children.text)
            except:
                pass
        if res:
            result.append(res)
    return result
