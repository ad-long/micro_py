"""get all trade codes of sz/sh
url: http://127.0.0.1:5000/code/sz
     http://127.0.0.1:5000/code/sh
     
result: 000001: 平安银行
        600000: 浦发银行
        code: name
"""

from flask import Flask
import requests
import json


app = Flask(__name__)

def __get_val(map_val:map):
    key = map_val["f12"]
    values = map_val["f14"]
    return {key:values}

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
        return {}

    result = resp.json()
    if not result["data"] or not result["data"]["diff"]:
        return {}

    result = map(__get_val,result["data"]["diff"])
    return json.dumps(list(result))

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
        return {}

    result = resp.json()
    if "data" not in result or "diff" not in result["data"]:
        return {}

    result = map(__get_val,result["data"]["diff"])
    return json.dumps(list(result))
