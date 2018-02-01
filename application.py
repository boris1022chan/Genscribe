from flask import Flask, jsonify, Response
from flask import request as req
import main
import urllib.request
import urllib3
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

    header = req.headers
    if header['Content-Type'] == 'application/json':
        randomNum = random.randint(1, 1001)
        name = 'file'+str(randomNum)+'.mp3'
        url = req.json['link']
        audio_file = urllib.request.urlretrieve(url, name)
        audioOpen = open(name, 'rb')
        process = main.TranscriptAnalyzer(audioOpen, 'audio/mp3')
        return str(process.frequently_discussed_topics())
        # return jsonify({'name': name})

    elif header['Content-Type'].startswith('audio'):
        process = main.TranscriptAnalyzer(req.data, header['Content-Type'])
        return str(process.frequently_discussed_topics())


if __name__ == '__main__':
    application.run(host='0.0.0.0')
