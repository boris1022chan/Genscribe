from flask import Flask, jsonify
from flask import request


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

links = []

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'links': links})


@app.route('/insert', methods=['POST'])
def create_task():

    header = request.headers
    print("CONTENT TYPE: " + header['Content-Type'])
    link = {
        'link': request.json['link']

    }
    links.append(link)
    return jsonify({'link': link}), 201


if __name__ == '__main__':
    app.run(debug=True)
