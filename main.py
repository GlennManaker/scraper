import time
import requests
import threading
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from api import stats_endpoint

load_dotenv()

THREADS = int(os.getenv('THREADS_FOR_PARSE'))
_cm = []
for i in range(THREADS):
    _cm.append([])

server = Flask(__name__)

count_threads = 0

start_time = time.time()

client = MongoClient(os.getenv('MONGO_CLIENT'))

db_m = client.matches
_mM = db_m['statistic']

def parse(number):
    for el in _cm[number]:
        _m = requests.get(str(el))
        try:
            # _mM.insert_one({"url" : el, "keys" : _m.json()['Value']['SC']['S']})
            continue
        except:
            continue
        time.sleep(0.1)

def scraper():
    while (True):
        _m = requests.get(os.getenv('MAIN_PARSE_URL'))
        k = 0
        for el in _m.json()['Value']:
            _cm[k%THREADS].append(os.getenv('URL_GET_GAME').format(str(el['I'])))
            k += 1

        threads = []
        for i in range(THREADS):
            _myt = threading.Thread(target=parse, args=(i,))
            threads.append(_myt)
            _myt.start()


server.register_blueprint(stats_endpoint)

if __name__ == "__main__":

    # _s = threading.Thread(target = scraper)
    # _s.start()

    server.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))