from flask import jsonify
import time


def stand_response_ok(cols: object, data: object):
    return jsonify(status="ok", ts=get_ts_ms(), cols=cols, data=data)


def stand_response_error(data: object):
    return jsonify(status="error", ts=get_ts_ms(), data=data)


def get_ts_ms():
    return int(time.time()*1000)


def get_ts_s():
    return int(time.time())


def get_ts_m():
    return int(time.time()/60)


def get_ts_h():
    return int(time.time()/(60*60))


def get_ts_d():
    return int(time.time()/(60*60*24))
