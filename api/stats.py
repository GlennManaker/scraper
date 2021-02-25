from flask import Blueprint, jsonify, request
import os
from . import stats_endpoint
from main import _mM

@stats_endpoint.route("/api/get_stats/<int:id>", methods=['GET'])
def get_stats(id):
    _r_q = request.args.get('filter')
    _info = _mM.find({'I': id})
    data = []
    for _t in _info:
        if (_r_q is not None):
            values = []
            for _e in _t['S']:
                print(_r_q)
                if (_r_q in _e['Key']):
                    print(_e)
                    values.append(_e)
            data.append({'time': _t['TS'], 'I': _t['I'], 'value': values})
        else:
            data.append({'time': _t['TS'], 'I': _t['I'], 'values': _t['S']})
    return jsonify(data)


@stats_endpoint.route("/api/available_ids", methods=['GET'])
def get_available_id():
    data = []
    _info = _mM.distinct("I")
    for _t in _info:
        print(_t)
        data.append(_t)
    return jsonify({'ids': data})
