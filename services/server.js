'use strict';

const express = require('express');
const WebSocket = require('ws');
const watson = require('watson-developer-cloud');
const cors = require('cors');
const bodyParser = require('body-parser');
const MicrophoneStream = require('microphone-stream');
const getUserMedia = require('get-user-media-promise');
const request = require('https').request;
const http = require('http');
var micStream;

const app = express();

app.use(cors());
app.use(bodyParser.json());

// speech to text token endpoint
var sttAuthService = new watson.AuthorizationV1(
  {
    username: process.env.SPEECH_TO_TEXT_USERNAME || "914c12e3-abe4-4763-95a9-0fd97120d043",
    password: process.env.SPEECH_TO_TEXT_PASSWORD || "YSM7q8n6cXiC"
  }
);

// Token server
app.use('/api/speech-to-text/token', function (req, res) {
  sttAuthService.getToken(
    { url: watson.SpeechToTextV1.URL },
    function (err, token) {
      if (err) {
        console.log('Error retrieving token: ', err);
        res.status(500).send('Error retrieving token');
        return;
      }
      res.send(token);
    }
  );
});

app.get("/api/start", function (req, res) {
  
});

app.get("/api/stop", function (req, res) {
});

app.post("/api/audioLink", function (req, res) {
  // TODO: Add logic for audio link
  const URL = req.body.link;
  // console.log(JSON.stringify(req.body));
  request(URL, function (res) {
    console.log(JSON.stringify(res));
  })
  res.send("URL: " + URL);
});

app.post("/api/audioFile", function (req, res) {
  // TODO: Add logic for audio file
});

// set port to 3001 since React Dev Server runs on 3000
const port = process.env.PORT || 3001;
const server = http.createServer(app);
const wss = new WebSocket.Server({ server }, function () {
  console.log('Server is up at http://localhost:%s/', port);
});
 
wss.on('connection', function (ws) {
  ws.on('message', function (message) {
    // TODO: Direct stream to Watson Speech-to-text
    console.log('Received: %s', message);
    ws.send(JSON.stringify({"test": JSON.stringify(message)}));
  });
  ws.on('error', function (err) {
    console.log("Error: " + JSON.stringify(err));
  });
});

server.listen(port, function () {
  console.log('Listening on %d', port);
});