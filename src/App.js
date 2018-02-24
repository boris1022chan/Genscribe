import React, { Component } from 'react';
import logo from './logo.png';
import './App.css';
import recognizeMic from 'watson-speech/speech-to-text/recognize-microphone';

class App extends Component {
  constructor() {
    super();
    this.state = {};
    this.startRecording = this.startRecording.bind(this);
    this.stopRecording = this.stopRecording.bind(this);
    this.sendAudioFile = this.sendAudioFile.bind(this);
  }

  startRecording = () => {
    fetch('http://localhost:3002/api/speech-to-text/token')
      .then(function (response) {
        return response.text();
      }).then((token) => {
        console.log(token);
        this.stream = recognizeMic({
          token: token,
          objectMode: true, // send objects instead of text
          extractResults: true, // convert {results: [{alternatives:[...]}], result_index: 0} to {alternatives: [...], index: 0}
          format: false // optional - performs basic formatting on the results such as capitals an periods
        });
        this.stream.on('data', (data) => {
          // Send to backend for processing
          this.setState({
            text: data.alternatives[0].transcript
          })
        });
        this.stream.on('error', function (err) {
          console.log(err);
        });
        this.stream.stop.bind(this.stream);
      }).catch(function (error) {
        console.log(error);
      });
  }

  stopRecording = () => {
    this.stream.stop();
  }

  sendAudioFile = () => {
    var url = window.location.protocol + "//" + window.location.host + "/insert";
    console.log("URL: " + url);
    fetch({
      url: url,
      type: 'POST',
      data: JSON.stringify({ link: "https://s3.amazonaws.com/jzxhuang.com/test.mp3" }),
      headers: { "Content-Type": "application/json" },
      success: function (a, b, c) {
        console.log("Successfully sent POST req");
      },
      error: function (a, b, c) {
        alert('Fail to analyze audio. Please input a valid format');
      },
    });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} alt="genscribe logo" className="logo" />
          <h1 className="App-title">Welcome to Genscribe</h1>
        </header>
        <div className="content">
          <div>
            <h3> The best audio analyser for your meeting </h3>
            <form onSubmit={this.sendAudioFile}>
              <div className="userInput">
                <input id="typeInput" type="text" placeholder="https://s3.amazonaws.com/jzxhuang.com/test.mp3" autoComplete="off" />
                <input id="fileInput" type="file" />
              </div>
              <div className="submit-container">
                <input id="submit" type="submit" value="Submit" />
              </div>
            </form>

            <button onClick={this.startRecording}>Start Recording</button>
            <div style={{ fontSize: '40px' }}>{this.state.text}</div>
          </div>
          <button onClick={this.stopRecording}>Stop Recording</button>
        </div>
      </div>
    );
  }
}

export default App;
