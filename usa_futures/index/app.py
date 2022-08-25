"""get mim kline data within a day
url: gethttp://127.0.0.1:5000/usa_futures/index/nq
     
response(json):
{
    "status":"ok",
    "ts":1661410067366,
    "cols":{
        "ts":[
            "close",
            "vol"
        ]
    },
    "data":[
        {
            "1661378400000":[
                "12946.875",
                "224"
            ]
        },
        {
            "1661378460000":[
                "12949.800",
                "94"
            ]
        }
    ]
}
"""


from cachetools import cached, TTLCache
from datetime import datetime
import time
from flask import Flask
import requests
import sys
sys.path.append("../..")
from utils.response import stand_response_ok, stand_response_error


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


def __to_json(min_data: list):
    ts = min_data[-1]
    ts = time.mktime(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").timetuple())
    ts = (int)(ts*1000)
    close = min_data[-5]
    vol = min_data[-4]
    return {ts: [close, vol]}


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/usa_futures/index/<string:code>", methods=['GET'])
def kline_sz(code):
    url = f'https://stock2.finance.sina.com.cn/futures/api/openapi.php/GlobalFuturesService.getGlobalFuturesMinLine?symbol={code}'
    headers = {
        "Accept-Encoding": "gzip, deflate, sdch",
        "Referer": "https://finance.sina.com.cn",
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
    if "result" not in result or "status" not in result["result"] or result['result']['status']['code'] != 0 \
            or 'data' not in result['result'] or 'minLine_1d' not in result["result"]['data']:
        return stand_response_error(None)
    
    cols = {'ts': ['close', 'vol']}
    result = map(__to_json, result["result"]["data"]['minLine_1d'])
    return stand_response_ok(cols, list(result))
