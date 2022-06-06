"""sent email
url: post http://127.0.0.1:5000/email
     
body(json): 
{
    "from_smt_server":"smtp.qq.com",
    "from_email":"xxx@qq.com",
    "from_pwd":"xxx",
    "subject":"xxx",
    "to_user_list":"xxx@qq.com;xxx@163.com",
    "msg":"xxx"
}

response(json):
{
    "code": "ok",
    "ts": 1654073447104,
    "data": null
}
"""


from flask import Flask,request
import sys
sys.path.append("..")
from utils.response import stand_response_ok,stand_response_error
import smtplib
from email.mime.text import *
from email.mime.multipart import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/email", methods=['POST'])
def send_email():
    req = request.json
    params= ["from_smt_server", "from_email", "from_pwd",
             "subject", "to_user_list", "msg"]
    msg = ""
    for item in params:
        if item not in req:
            msg += "," + item
    if msg != "":
        return stand_response_error("request need params:" + msg[1:])
    
    content = MIMEMultipart()
    content['Subject'] = req["subject"]
    content['From'] = req["from_email"]
    content['To'] = req["to_user_list"]
    
    plain_msg = MIMEText(req["msg"], _subtype='plain', _charset='utf8')
    content.attach(plain_msg)

    s = smtplib.SMTP_SSL(req["from_smt_server"])
    s.login(req["from_email"], req["from_pwd"])
    s.sendmail(req["from_email"], req["to_user_list"].split(";"), content.as_string())
    s.close()

    return stand_response_ok(None)
