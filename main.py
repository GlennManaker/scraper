import time
import requests
import threading
from pymongo import MongoClient
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from api import stats_endpoint
from dotenv import load_dotenv
from concurrent import futures
from requests_futures import sessions
from matchX import matchX
load_dotenv()
THREADS = 2
_cm = []

server = Flask(__name__)
CORS(server)

count_threads = 0

start_time = time.time()

client = MongoClient(
    'mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority')

db_m = client.matches
_mM = db_m['statistic']



def scraper():
    while True:
        try:
            start_time = time.time()
            _m = requests.get('https://1xbet.com/LiveFeed/Get1x2_VZip?sports=1&count=1000&mode=4&country=2')
            session = sessions.FuturesSession(max_workers=32)
            future = [
                session.get('https://1xbet.com/LiveFeed/GetGameZip?id={}&lng=en'.format(str(el['I'])))
                for el in _m.json()['Value']
            ]

            for f in future:
                try:
                    _m = matchX(f.result().json()['Value'])
                    _mM.insert_one(_m.toDict())
                except:
                    continue
            print(len(future))
            print("--- %s seconds ---" % (time.time() - start_time))
        except:
            continue


server.register_blueprint(stats_endpoint)
if __name__ == "__main__":
    _fSc = threading.Thread(target=scraper)
    _fSc.start()
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


