import time
import requests
import threading
from pymongo import MongoClient
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from api import stats_endpoint
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

load_dotenv()
THREADS = 2
_cm = []
for i in range(THREADS):
    _cm.append([])

server = Flask(__name__)
CORS(server)

count_threads = 0

start_time = time.time()

client = MongoClient('mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority')

db_m = client.matches
_mM = db_m['statistic']

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

server.register_blueprint(swaggerui_blueprint)

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

if __name__ == '__main__':
    #host="0.0.0.0", port=int(os.environ.get("PORT", 5000))
    server.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))