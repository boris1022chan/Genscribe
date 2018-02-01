import os.path
from flask import Flask, Response, jsonify
from flask import request
import urllib.request
import random

application = Flask(__name__)
application.debug=True

links = []
audio_file = None


@application.route('/', methods=['GET'])
def welcome():
    content = open('./src/index.html').read()
    return Response(content, mimetype="text/html")


@application.route('/insert', methods=['POST'])
def create_task():

    header = request.headers
    if header['Content-Type'] == 'application/json':
        name = 'file'+str(random.randint(1, 1001))
        url = request.json['link']
        audio_file = urllib.request.urlretrieve(url, name)
        return jsonify({'name': name})

    elif header['Content-Type'].startswith('audio'):
        audio_file = request.json['file']


if __name__ == '__main__':
    application.run(host='0.0.0.0')
