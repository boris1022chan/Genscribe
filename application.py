from flask import Flask, jsonify, Response, abort, url_for
from flask import request as req
import main
import urllib.request
import urllib3
import random
import os

application = Flask(__name__)
application.debug=True

links = []
extensions = ['.mp3', '.wav', '.flac']



@application.route('/', methods=['GET'])
def welcome():
    # content = open('./src/index.html').read()
    # return Response(content, mimetype="text/html")
    # url_for('static', filename='requirements.txt')
    # url_for('static', filename='english.pickle')
    return main._output()

@application.route('/insert', methods=['POST', 'GET'])
def create_task():
    # myObj = main.myClass()
    # return myObj._out()
    header = req.headers
    if header['Content-Type'] == 'application/json':
        # return ("link")
        randomNum = random.randint(1, 1001)
        url = req.json['link']
        audio_type = os.path.splitext(url)[1].lower()
        valid_file = False
        for item in extensions:
            if audio_type == item:
                valid_file = True
                break
        if not valid_file:
            return "please enter a url with valid audio file."
        # name = 'file' + str(randomNum) + '.mp3'
        # audio_file = urllib.request.urlretrieve(url, name)
        # audioOpen = open(name, 'rb')
        audio_type = 'audio/' + audio_type.split(".")[-1]
        audio_file = urllib.request.urlopen(url)
        process = main.TranscriptAnalyzer(audio_file, audio_type)
        return str(process.frequently_discussed_topics()), 200
        # return jsonify({'name': name})

    elif header['Content-Type'].startswith('audio'):
        process = main.TranscriptAnalyzer(req.data, header['Content-Type'])
        return str(process.frequently_discussed_topics()), 200

    abort(400)


@application.errorhandler(400)
def page_not_found(error):
    return str("fail to analyze audio"), 400


if __name__ == '__main__':
    application.run(host='0.0.0.0')
