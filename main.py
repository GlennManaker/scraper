import time

import requests
import threading
from pymongo import MongoClient

_cm = [[], [], [], [], []]

start_time = time.time()

client = MongoClient("mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority")

db_m = client.matches
_mM = db_m['statistic']

def parse(number):
    for el in _cm[number]:
        _m = requests.get(str(el))
        try:
            _mM.insert_one({"url" : el, "keys" : _m.json()['Value']['SC']['S']})
        except:
            continue
        time.sleep(0.1)

if __name__ == "__main__":
    while (True):
        _m = requests.get('https://1xbet.com/LiveFeed/Get1x2_VZip?sports=1&count=1000&mode=4&country=2')
        k = 0
        for el in _m.json()['Value']:
            if (k % 5 == 0):
                _cm[k % 5].append('https://1xbet.com/LiveFeed/GetGameZip?id=' + str(el['I']) + '&lng=en')
            if (k % 5 == 1):
                _cm[k % 5].append('https://1xbet.com/LiveFeed/GetGameZip?id=' + str(el['I']) + '&lng=en')
            if (k % 5 == 2):
                _cm[k % 4].append('https://1xbet.com/LiveFeed/GetGameZip?id=' + str(el['I']) + '&lng=en')
            if (k % 5 == 3):
                _cm[k % 5].append('https://1xbet.com/LiveFeed/GetGameZip?id=' + str(el['I']) + '&lng=en')
            if (k % 5 == 4):
                _cm[k % 5].append('https://1xbet.com/LiveFeed/GetGameZip?id=' + str(el['I']) + '&lng=en')
            k = k + 1

        threads = []
        for i in range(5):
            print(i)
            _myt = threading.Thread(target=parse, args=(i,))
            threads.append(_myt)
            _myt.start()

        for i in range(5):
            threads[i].join()