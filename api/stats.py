from flask import Blueprint, jsonify, request
import os
from . import stats_endpoint
from main import _mM

@stats_endpoint.route("/api/get_stats/<int:id>", methods=['GET'])
def get_stats(id):
    _r_q = request.args.get('filter')
    _info = _mM.find({'url': os.getenv('URL_GET_GAME').format(id)})
    data = []
    for _t in _info:
        if (_r_q is not None):
            values = []
            for _e in _t['keys']:
                print(_r_q)
                print(_e['Key'])
                if (_r_q in _e['Key']):
                    print(_e)
                    values.append(_e)
            data.append({'time': int(_t['_id'].generation_time.timestamp()), 'url': _t['url'], 'value': values})
        else:
            data.append({'time': int(_t['_id'].generation_time.timestamp()), 'url': _t['url'], 'values': _t['keys']})
    return jsonify(data)


@stats_endpoint.route("/api/available_ids", methods=['GET'])
def get_available_id():
    data = []
    _info = _mM.distinct("url")
    for _t in _info:
        data.append(_t[_t.find('=') + 1:_t.find('&')])
    return jsonify({'ids': data})
