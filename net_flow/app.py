"""get net flow top N
url: get http://127.0.0.1:5000/net_flow/sz/10
     get http://127.0.0.1:5000/net_flow/sh/10
     
response(json):
{
    "code": "ok",
    "ts": 1654073625977,
    "data": [["300059","东方财富",1342650304.0,1456423712.0,2018703664.0]]
}
[code,name,today inflow,3day inflow,5day inflow]
"""


from flask import Flask
import requests
import sys
sys.path.append("..")
from utils.response import stand_response_ok,stand_response_error

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/net_flow/sz/<int:top>", methods=['GET'])
def net_flow_sz(top):
    size = 3*top if top < 10 else 2*top
    result = []
    
    url = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f267&po=1&pz={size}&pn=1&np=1&fltt=2&invt=2&fs=m:0+t:6,m:0+t:80&fields=f12,f14,f62,f267,f164,f174'
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
        return stand_response_error(None)
        
    data = jdata['data']['diff']
    for item in data:
        instance = []
        instance.append(item['f12'])  # code
        instance.append(item['f14'])  # name
        instance.append(item['f62'])  # today inflow(今日主力净流入)
        instance.append(item['f267'])  # 3day inflow(3日主力净流入)
        instance.append(item['f164'])  # 5day inflow(5日主力净流入)
        # instance.append(item['f174'])  # 10day inflow(10日主力净流入)
        if instance[1].startswith('*') or instance[1].startswith('ST') or instance[1].startswith('N'):
            continue
        if instance[2] == '-' or instance[3] == '-' or instance[4] == '-' or instance[4] == '-':
            continue
        if instance[2] > 0 and (instance[3] - instance[2]) > 0 and (instance[4] - instance[3]) > 0:
            result.append(instance)
        if len(result) >= top:
            break
    return stand_response_ok(result)


@app.route("/net_flow/sh/<int:top>", methods=['GET'])
def net_flow_sh(top):
    size = 3*top if top < 10 else 2*top
    result = []
    
    url = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f267&po=1&pz={size}&pn=1&np=1&fltt=2&invt=2&fs=m:1+t:2,m:1+t:23&fields=f12,f14,f62,f267,f164,f174'
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
        return stand_response_error(None)

    data = jdata['data']['diff']
    for item in data:
        instance = []
        instance.append(item['f12'])  # code
        instance.append(item['f14'])  # name
        instance.append(item['f62'])  # today inflow(今日主力净流入)
        instance.append(item['f267'])  # 3day inflow(3日主力净流入)
        instance.append(item['f164'])  # 5day inflow(5日主力净流入)
        # instance.append(item['f174'])  # 10day inflow(10日主力净流入)
        if instance[1].startswith('*') or instance[1].startswith('ST') or instance[1].startswith('N'):
            continue
        if instance[2] == '-' or instance[3] == '-' or instance[4] == '-' or instance[4] == '-':
            continue
        if instance[2] > 0 and (instance[3] - instance[2]) > 0 and (instance[4] - instance[3]) > 0:
            result.append(instance)
        if len(result) >= top:
            break
    return stand_response_ok(result)
