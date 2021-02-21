from flask import Blueprint, jsonify
import os
from . import stats_endpoint
from main import _mM

@stats_endpoint.route("/api/get_stats/<id>", methods = ['GET'])
def get_stats(id):
    _info = _mM.find({'url' : os.getenv('URL_GET_GAME').format(id)})
    data = []
    for _t in _info:
        data.append({'time' : int(_t['_id'].generation_time.timestamp()), 'url' : _t['url'], 'values' : _t['keys']})
    return jsonify(data)