"""get net flow top N
url: get http://127.0.0.1:5000/trade_info/sz/000001
     get http://127.0.0.1:5000/trade_info/sh/600000
     
response(json):
{
    "code":"ok",
    "data":[
        "600000",
        19388000000,
        230708070827.46002,
        0.4,
        50002000000,
        0.9692661847,
        3.695780071669,
        19991110
    ],
    "ts":1654501503994
}
[代码,净利润,流通市值,市净率,总营收,总营收同比,净利润同比,上市时间]
"""


from flask import Flask
import requests
import sys
sys.path.append("..")
from utils.response import stand_response_ok,stand_response_error

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/trade_info/sz/<string:code>", methods=['GET'])
def trade_info_sz(code):
    if not code.startswith('00') and not code.startswith('30'):
        return stand_response_error(f"{code} is not sz code.")
    lcode = '0.' + code
    url = 'https://push2.eastmoney.com/api/qt/stock/get?&invt=2&fltt=2&fields=f57,f105,f117,f167,f183,f184,f185,f189&secid={0}'.format(lcode)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    
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

    jdata = resp.json()
    if 'data' not in jdata.keys():
        return result
    data = jdata['data']

    result = []
    result.append(data['f57'])  # 代码
    result.append(data['f105'])  # 净利润
    result.append(data['f117'])  # 流通市值
    result.append(data['f167'])  # 市净率
    result.append(data['f183'])  # 总营收
    result.append(data['f184'])  # 总营收同比
    result.append(data['f185'])  # 净利润同比
    result.append(data['f189'])  # 上市时间

    return stand_response_ok(result)


@app.route("/trade_info/sh/<string:code>", methods=['GET'])
def trade_info_sh(code):
    if not code.startswith('60') and not code.startswith('6'):
        return stand_response_error(f"{code} is not sh code.")
    lcode = '1.' + code
    url = 'https://push2.eastmoney.com/api/qt/stock/get?&invt=2&fltt=2&fields=f57,f105,f117,f167,f183,f184,f185,f189&secid={0}'.format(lcode)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    
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

    jdata = resp.json()
    if 'data' not in jdata.keys():
        return result
    data = jdata['data']

    result = []
    result.append(data['f57'])  # 代码
    result.append(data['f105'])  # 净利润
    result.append(data['f117'])  # 流通市值
    result.append(data['f167'])  # 市净率
    result.append(data['f183'])  # 总营收
    result.append(data['f184'])  # 总营收同比
    result.append(data['f185'])  # 净利润同比
    result.append(data['f189'])  # 上市时间

    return stand_response_ok(result)
