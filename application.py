from flask import Flask, jsonify, Response
from flask import request as req
from flask_cors import CORS
import main
import urllib.request
# import urllib3
import random

application = Flask(__name__)
application.debug=True
CORS(application)

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
        name = 'file'+str(random.randint(1, 1001))
        url = req.get_json()['link']
        # audio_file = urllib.request.urlretrieve(url, name)
        return jsonify({'url': url})
        # return jsonify({'name': name})

    elif header['Content-Type'].startswith('audio'):
        process = main.TranscriptAnalyzer(req.data, header['Content-Type'])
        return str(process.frequently_discussed_topics())


if __name__ == '__main__':
    application.run(host='0.0.0.0')
