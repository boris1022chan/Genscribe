import json
from pprint import pprint

file_directory = './json_data'

json_data = open(file_directory).read()

data = json.loads(json_data)

class TranscriptAnalyzer:
    def __init__(self, json_data):
        self.sentence_blocks = []
        for result in data['results']:
            self.sentence_blocks.append(result['alternatives'][0]['transcript'])

var = TranscriptAnalyzer(json_data=json_data)
print(var.sentence_blocks)
print(json.dumps(data, indent=4, sort_keys=True))