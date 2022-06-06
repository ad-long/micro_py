"""get all trade codes of sz/sh
url: get http://127.0.0.1:5000/code/sz
     get http://127.0.0.1:5000/code/sh
     
response(json):
{
    "code": "ok",
    "ts": 1654073761668,
    "data": [
        {
            "300370": "*ST安控"
        }
    ]
}
code: name
"""

from flask import Flask
import requests
import sys
sys.path.append("..")
from utils.response import stand_response_ok,stand_response_error,get_ts_h
from cachetools import cached,Cache

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def __get_val(map_val:map):
    key = map_val["f12"]
    values = map_val["f14"]
    return {key:values}

@cached(cache= {}, key=get_ts_h)
@app.route("/code/sz", methods=['GET'])
def code_sz():
    page_size = 10000

    url = f"https://54.push2.eastmoney.com/api/qt/clist/get?pn=1&pz={page_size}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80&fields=f12,f14"
    headers = {
        "Accept-Encoding": "gzip, deflate, sdch",
        "Referer": "http://quote.eastmoney.com/",
        "Connection": "keep-alive",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/54.0.2840.100 "
            "Safari/537.36"
        ),
    }
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        return stand_response_error(None)

    result = resp.json()
    if not result["data"] or not result["data"]["diff"]:
        return stand_response_error(None)

    result = map(__get_val,result["data"]["diff"])
    return stand_response_ok(list(result))


@cached(cache= {}, key=get_ts_h)
@app.route("/code/sh", methods=['GET'])
def code_sh():
    page_size = 10000

    url = f"https://54.push2.eastmoney.com/api/qt/clist/get?pn=1&pz={page_size}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f12,f14"
    headers = {
        "Accept-Encoding": "gzip, deflate, sdch",
        "Referer": "http://quote.eastmoney.com/",
        "Connection": "keep-alive",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/54.0.2840.100 "
            "Safari/537.36"
        ),
    }
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        return stand_response_error(None)

    result = resp.json()
    if "data" not in result or "diff" not in result["data"]:
        return stand_response_error(None)

    result = map(__get_val,result["data"]["diff"])
    return stand_response_ok(list(result))
