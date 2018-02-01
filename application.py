from flask import Flask, jsonify
from flask import request
import urllib
import random

application = Flask(__name__)
application.debug=True

links = []
audio_file = None


@application.route('/', methods=['GET'])
def welcome():
    return jsonify({'links': links})


@application.route('/insert', methods=['GET', 'POST'])
def create_task():

    header = request.headers
    if header['Content-Type'] == 'application/json':
        name = 'file'+str(random.randint(1, 1001))
        url = request.json['link']
        audio_file = urllib.urlretrieve(url, name)
        return jsonify({'name': name})

    elif header['Content-Type'].startswith('audio'):
        print("")

    # print("CONTENT TYPE: " + header['Content-Type'])
    # link = {
    #     'link': request.json['link']
    #
    # }
    # links.append(link)
    # return jsonify({'link': link}), 201


if __name__ == '__main__':
    application.run(host='0.0.0.0')
