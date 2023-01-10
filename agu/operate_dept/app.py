"""get daily kline data within a year
url: get http://127.0.0.1:5000/agu/operate_dept
     
response(json):
{
    "status":"ok",
    "ts":1672992515443,
    "cols":{
        "symbol":[
            "name",
            "operate_dept_qty",
            "rise(%)"
        ]
    },
    "data":{
        "0.002095":[
            "生 意 宝",
            10,
            -7.28
        ],
        "1.600520":[
            "文一科技",
            10,
            -7.55
        ],
        "0.000153":[
            "丰原药业",
            10,
            -2.46
        ]
}
"""


from cachetools import cached, TTLCache
from flask import Flask
import requests
import sys
from datetime import date, timedelta
import time
from retry import retry
sys.path.append("../..")
from utils.response import stand_response_ok, stand_response_error


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

__HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


@retry(requests.exceptions.SSLError, tries=3, delay=1)
def get_operate_dept() -> map:
  today = date.today()-timedelta(days=1)
  d1 = today.strftime("%Y-%m-%d")
  # d1 = '2023-01-06'
  url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TOTAL_NETAMT,ONLIST_DATE,OPERATEDEPT_CODE&sortTypes=-1,-1,1&pageSize=1000&pageNumber=1&reportName=RPT_OPERATEDEPT_ACTIVE&columns=ALL&source=WEB&client=WEB&filter=(ONLIST_DATE>='{d1}')"
  # print(url)
  resp = requests.get(url, headers=__HEADERS)
  jdata = resp.json()
  if jdata['code'] != 0:
    return None

  result = {}
  data = jdata['result']['data']
  for item in data:
    one_dept_symbol_list = item['BUY_STOCK']
    temp_list = one_dept_symbol_list.split(' ')
    for symbol in temp_list:
      if symbol.endswith('.SZ'):
        symbol = symbol.replace('.SZ', '')
        symbol = f'0.{symbol}'
      elif symbol.endswith('.SH'):
        symbol = symbol.replace('.SH', '')
        symbol = f'1.{symbol}'
      else:
        continue
      if symbol not in result:
        result[symbol] = 1
      else:
        result[symbol] += 1
  return result


@retry(requests.exceptions.SSLError, tries=3, delay=1)
def get_rise(symbol: str, size: int = 5) -> list:
  url = f"https://89.push2his.eastmoney.com/api/qt/stock/kline/get?secid={symbol}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt={size+1}"
  # print(url)
  resp = requests.get(url, headers=__HEADERS)
  jdata = resp.json()
  if jdata['data'] is None:
    return None

  code = jdata['data']['code']
  if code.startswith('6'):
    code = f'1.{code}'
  elif code.startswith('0') or code.startswith('3'):
    code = f'0.{code}'
  else:
    return None

  name = jdata['data']['name']
  data = jdata['data']['klines']
  if len(data) != size+1:
    return None

  avg5 = 0
  for i in range(size):
    one_kline = data[i]
    temp_list = one_kline.split(',')
    close = float(temp_list[1])
    avg5 += float(close)
  avg5 /= size

  pre_date = data[-2]
  temp_list = pre_date.split(',')
  pre_open = float(temp_list[1])
  pre_close = float(temp_list[2])

  cur_date = data[-1]
  temp_list = cur_date.split(',')
  cur_close = float(temp_list[2])
  if pre_open <= avg5 and pre_close >= avg5:
    rise = round((cur_close-pre_open)/pre_open*100, 2)
    result = [code, name, rise]
    # print(name, cur_close, pre_open)
    return result
  else:
    return None


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/agu/operate_dept", methods=['GET'])
def operate_dept():
    operate_dept_symbl = get_operate_dept()

    temp_rise = map(lambda x: get_rise(x, 5), operate_dept_symbl.keys())
    temp_rise = list(temp_rise)

    map_rise = {}
    for item in temp_rise:
      if item is None:
        continue
      map_rise[item[0]] = [item[1], item[2]]

    result = {}
    for symbol, others in map_rise.items():
      qty = operate_dept_symbl[symbol]
      result[symbol] = [map_rise[symbol][0], qty, map_rise[symbol][1]]
    result = dict(
        sorted(result.items(), key=lambda item: item[1][1], reverse=True))
    cols = {'symbol': ['name', 'operate_dept_qty', 'rise(%)']}
    return stand_response_ok(cols, result)
