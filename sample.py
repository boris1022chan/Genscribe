import requests

url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
headers = {'Content-Type': 'audio/flac'}
files = {'data-binary': open('./audio-file.flac', 'rb')}

res = requests.post(url, auth=('914c12e3-abe4-4763-95a9-0fd97120d043', 'YSM7q8n6cXiC'), headers=headers, files=files)

print(res.text)


#{
#  "url": "https://stream.watsonplatform.net/speech-to-text/api",
#  "username": "914c12e3-abe4-4763-95a9-0fd97120d043",
#  "password": "YSM7q8n6cXiC"
#}