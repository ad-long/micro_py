from flask import jsonify

def stand_response_ok(data:object):
    return jsonify(code="ok", data=data)

def stand_response_error(data:object):
    return jsonify(code="error", data=data)
