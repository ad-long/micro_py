"""get net flow top N order by 3day net inflow desc
url: get http://127.0.0.1:5000/agu/net_flow/sz/10
     get http://127.0.0.1:5000/agu/net_flow/sh/10
     
response(json):
{
    "status":"ok",
    "ts":1661409675678,
    "cols":{
        "code":[
            "today inflow",
            "3day inflow",
            "5day inflow",
            "name"
        ]
    },
    "data":[
        {
            "002714":[
                121459104,
                459015210,
                711982826,
                "牧原股份"
            ]
        },
        {
            "002385":[
                227562192,
                449765289,
                481842943,
                "大北农"
            ]
        }
    ]
}
"""


from cachetools import cached, TTLCache
from flask import Flask
import requests
import sys
sys.path.append("../..")
from utils.response import stand_response_ok, stand_response_error

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/agu/net_flow/sz/<int:top>", methods=['GET'])
def net_flow_sz(top):
    size = 10*top if top < 10 else 5*top
    result = []

    url = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f267&po=1&pz={size}&pn=1&np=1&fltt=2&invt=2&fs=m:0+t:6,m:0+t:80&fields=f12,f14,f62,f267,f164'
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
        code = item['f12']  # code
        name = item['f14']  # name

        in_flows = []
        in_flows.append(item['f62'])  # today inflow(今日主力净流入)
        in_flows.append(item['f267'])  # 3day inflow(3日主力净流入)
        in_flows.append(item['f164'])  # 5day inflow(5日主力净流入)
        in_flows.append(name)
        if name.startswith('*') or name.startswith('ST') or name.startswith('N'):
            continue
        if in_flows[0] == '-' or in_flows[1] == '-' or in_flows[2] == '-':
            continue
        if in_flows[0] > 0 and (in_flows[1] - in_flows[0]) > 0 and (in_flows[2] - in_flows[1]) > 0:
            result.append({code: in_flows})
        if len(result) >= top:
            break

    cols = {'code': ['today inflow', '3day inflow', '5day inflow', 'name']}
    return stand_response_ok(cols, result)


@cached(cache=TTLCache(maxsize=None, ttl=1))
@app.route("/agu/net_flow/sh/<int:top>", methods=['GET'])
def net_flow_sh(top):
    size = 10*top if top < 10 else 5*top
    result = []

    url = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f267&po=1&pz={size}&pn=1&np=1&fltt=2&invt=2&fs=m:1+t:2,m:1+t:23&fields=f12,f14,f62,f267,f164'
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
        code = item['f12']  # code
        name = item['f14']  # name

        in_flows = []
        in_flows.append(item['f62'])  # today inflow(今日主力净流入)
        in_flows.append(item['f267'])  # 3day inflow(3日主力净流入)
        in_flows.append(item['f164'])  # 5day inflow(5日主力净流入)
        in_flows.append(name)
        if name.startswith('*') or name.startswith('ST') or name.startswith('N'):
            continue
        if in_flows[0] == '-' or in_flows[1] == '-' or in_flows[2] == '-':
            continue
        if in_flows[0] > 0 and (in_flows[1] - in_flows[0]) > 0 and (in_flows[2] - in_flows[1]) > 0:
            result.append({code: in_flows})
        if len(result) >= top:
            break

    cols = {'code': ['today inflow', '3day inflow', '5day inflow', 'name']}
    return stand_response_ok(cols, result)
