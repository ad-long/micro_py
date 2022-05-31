"""get daily kline data within a year
url: http://127.0.0.1:5000/kline/sz/000001
     http://127.0.0.1:5000/kline/sh/600000
     
result: 2022-05-31: 14.07,14.16,14.18,14.00,938869,1325012048.00,1.28,0.57,0.08,0.48
        2022-05-31: 7.90,7.94,7.98,7.88,317509,251916051.00,1.27,0.76,0.06,0.11
        date: open,close,high,low,vol,amount,h-l(p),c-o(p),gain(amount),gain(p)
"""


from flask import Flask
import requests
import json


app = Flask(__name__)

def __to_json(kline_str:str):
    array_temp = kline_str.split(",")
    key = array_temp[0]
    values = array_temp[1:]
    return {key:values}

@app.route("/kline/sz/<string:code>", methods=['GET'])
def kline_sz(code):
    url = f'https://89.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.{code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt=365'
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
        return {}
    result = resp.json()
    if "data" not in result or "klines" not in result["data"]:
        return {}
    result = map(__to_json, result["data"]["klines"])
    return json.dumps(list(result))


@app.route("/kline/sh/<string:code>", methods=['GET'])
def kline_sh(code):
    url = f'https://89.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.{code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt=365'
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
        return {}
    result = resp.json()
    if "data" not in result or "klines" not in result["data"]:
        return {}
    result = map(__to_json, result["data"]["klines"])
    return json.dumps(list(result))
