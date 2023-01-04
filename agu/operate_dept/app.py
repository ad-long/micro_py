"""get daily kline data within a year
url: get http://127.0.0.1:5000/agu/operate_dept
     
response(json):
{
    "status":"ok",
    "ts":1672285276204,
    "cols":{
        "symbol":[
            "operate_dept_qty",
            "turnover_rate"
        ]
    },
    "data":{
        "亚星客车":[
            10,
            13.45
        ],
        "祥源文旅":[
            10,
            8.95
        ],
        "明牌珠宝":[
            10,
            7.68
        ],
        "玉龙股份":[
            10,
            7.48
        ]
    }
}
"""


from cachetools import cached, TTLCache
from flask import Flask
import requests
import sys
from datetime import date, timedelta
sys.path.append("../..")
from utils.response import stand_response_ok, stand_response_error


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

__HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def get_operate_dept() -> map:
  today = date.today()-timedelta(days=1)
  d1 = today.strftime("%Y-%m-%d")
  url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TOTAL_NETAMT,ONLIST_DATE,OPERATEDEPT_CODE&sortTypes=-1,-1,1&pageSize=1000&pageNumber=1&reportName=RPT_OPERATEDEPT_ACTIVE&columns=ALL&source=WEB&client=WEB&filter=(ONLIST_DATE>='{d1}')"
  # print(url)
  resp = requests.get(url, headers=__HEADERS)
  jdata = resp.json()
  if jdata['code'] != 0:
    return None

  result = {}
  data = jdata['result']['data']
  for item in data:
    one_dept_symbol_list = item['SECURITY_NAME_ABBR']
    temp_list = one_dept_symbol_list.split(' ')
    for symbol in temp_list:
      if symbol not in result:
        result[symbol] = 1
      else:
        result[symbol] += 1
  return result

def get_turnover_rate() -> map:
  url = f"http://18.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=3000&po=1&np=1&fltt=2&invt=2&fid=f8&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152"
  # print(url)
  resp = requests.get(url, headers=__HEADERS)
  jdata = resp.json()
  if jdata['data'] is None:
    return None

  result = {}
  data = jdata['data']['diff']
  for item in data:
    symbol = item['f14']
    tr = item['f8']
    result[symbol] = tr
  return result


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/agu/operate_dept", methods=['GET'])
def operate_dept():
    operate_dept_symbl = get_operate_dept()
    symbol_turnover_rata = get_turnover_rate()
    
    result = {}
    keys_ds = operate_dept_symbl.keys()
    keys_st = symbol_turnover_rata.keys()
    for item in keys_st:
        if item not in keys_ds:
            continue
        tr = symbol_turnover_rata[item]
        if tr < 0 or tr > 15:
          continue
        result[item] = [operate_dept_symbl[item], tr]
    result = dict(sorted(result.items(), key=lambda item: item[1][0], reverse=True))
    cols = {'symbol_name': ['operate_dept_qty', 'turnover_rate']}
    return stand_response_ok(cols, result)

