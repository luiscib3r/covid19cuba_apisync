import config
import requests
import time

from pymongo import MongoClient

client = MongoClient(config.MONGO_URI)

db = client.tbot

import json

def savedata(datahash, data):
    hashdoc = {'datahash': datahash}
    datadoc = {'data': data}

    lasthash = db.lasthash

    try:
        lastcode = [l for l in lasthash.find()][-1]['datahash']
    except:
        lastdata = db.lastdata
        lastdata.drop()
        lastdata.insert(datadoc)
        lasthash.drop()
        lasthash.insert(hashdoc)
        time.sleep(15)
        token = {'token': config.TOKEN}
        requests.post(config.API_URI, json=token)

        return

    if datahash != lastcode:
        lastdata = db.lastdata
        lastdata.drop()
        lastdata.insert(datadoc)
        lasthash.drop()
        lasthash.insert(hashdoc)
        time.sleep(15)
        requests.post(config.API_URI, json=token)


def getdata():
    col = db.lastdata

    doc = [d for d in col.find()][-1]

    data = json.loads(doc['data'])
    
    return data