import hashlib
import requests
import mdb

from config import DATA_URI, TOKEN

def update():
    try:
        data = requests.get(DATA_URI).content
    except:
        return 0

    hexcode = hashlib.md5(data).hexdigest()

    mdb.savedata(hexcode, data)

    return hexcode

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'COVID19 Cuba Data API Sync'
    })

@app.route('/sync', methods=['POST'])
def sync():
    code = update()

    data = request.get_json()

    if data['token'] == TOKEN:
        print(data)
    else:
        print('UPS')

    return jsonify({
        'code': code
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)