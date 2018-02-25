'use strict';

const express = require('express');
const app = express();
const watson = require('watson-developer-cloud');
const cors = require('cors');

app.use(cors())

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

app.post("/api/audioLink", function (req, res) {
  // TODO: Add logic for audio link
})

app.post("/api/audioFile", function (req, res) {
  // TODO: Add logic for audio file
})


// set port to 3001 since React Dev Server runs on 3000
const port = process.env.PORT || 3001;
app.listen(port, function () {
  console.log('Server is up at http://localhost:%s/', port);
});
