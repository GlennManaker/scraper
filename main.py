import time
import requests
import threading
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from api import stats_endpoint

load_dotenv()

THREADS = 2
_cm = []
for i in range(THREADS):
    _cm.append([])

server = Flask(__name__)

count_threads = 0

start_time = time.time()

client = MongoClient('mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority')

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
        _m = requests.get('https://1xbet.com/LiveFeed/Get1x2_VZip?sports=1&count=1000&mode=4&country=2')
        k = 0
        for el in _m.json()['Value']:
            _cm[k%THREADS].append('https://1xbet.com/LiveFeed/GetGameZip?id={}&lng=en'.format(str(el['I'])))
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