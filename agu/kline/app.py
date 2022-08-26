"""get daily kline data within a year
url: get http://127.0.0.1:5000/agu/kline/sz/000001
     get http://127.0.0.1:5000/agu/kline/sh/600000
     
response(json):
{
    "status":"ok",
    "ts":1661409491722,
    "cols":{
        "date":[
            "open",
            "close",
            "high",
            "low",
            "vol",
            "amount",
            "h-l(p)",
            "c-o(p)",
            "gain(amount)",
            "gain(p)"
        ]
    },
    "data":[
        {
            "2021-03-01":[
                "21.54",
                "21.45",
                "21.68",
                "21.18",
                "1125387",
                "2408050912.00",
                "2.34",
                "0.33",
                "0.07",
                "0.58"
            ]
        }
    ]
}
"""


from utils.response import stand_response_ok, stand_response_error
from cachetools import cached, TTLCache
from flask import Flask
import requests
import sys
sys.path.append("../..")

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

KLINE_SIZE = 365*3-116*2-115


def __to_json(kline_str: str):
    array_temp = kline_str.split(",")
    key = array_temp[0]
    values = array_temp[1:]
    return {key: values}


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/agu/kline/sz/<string:code>", methods=['GET'])
def kline_sz(code):
    global KLINE_SIZE
    
    url = f'https://89.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.{code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt={KLINE_SIZE}'
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
    if "data" not in result or "klines" not in result["data"]:
        return stand_response_error(None)

    cols = {'date': ['open', 'close', 'high', 'low', 'vol',
                     'amount', 'h-l(p)', 'c-o(p)', 'gain(amount)', 'gain(p)']}
    result = map(__to_json, result["data"]["klines"])
    return stand_response_ok(cols, list(result))


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/agu/kline/sh/<string:code>", methods=['GET'])
def kline_sh(code):
    url = f'https://89.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.{code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt={KLINE_SIZE}'
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
    if "data" not in result or "klines" not in result["data"]:
        return stand_response_error(None)

    cols = {'date': ['open', 'close', 'high', 'low', 'vol',
                     'amount', 'h-l(p)', 'c-o(p)', 'gain(amount)', 'gain(p)']}
    result = map(__to_json, result["data"]["klines"])
    return stand_response_ok(cols, list(result))
