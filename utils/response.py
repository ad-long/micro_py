from flask import jsonify
import time


def stand_response_ok(data:object):
    return jsonify(code="ok", data=data, ts=int(time.time()*1000))

def stand_response_error(data:object):
    return jsonify(code="error", data=data, ts=int(time.time()*1000))
