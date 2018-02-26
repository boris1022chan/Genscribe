![Genscribe logo](./frontend/src/logo.png)
### Summary of proposal:

No one wants to be the note taker at a meeting, or sit through an hour-long recording just to find a couple quips of information. That’s why we’re building Genscribe to take notes for you. It can be used in any context (Skype/ Call/ GoToMeeting/ In-person meeting). Genscribe gives a short summary of the meeting outlining the key topics discussed, upcoming deadlines, dates for any other meetings that were scheduled, and important decisions that were made. Since it will be built off a neural network model, it can also be extended to summarize other interactions, such as calls or emails.

### Summary of flow:

1. Take audio input

2. Convert audio to text using a Speech-to-Text API:

  o Speaker Detection is possible using IBM Watson API

3. Process the text and try to get some understanding of it (Natural Language Processing). We have two options for NLP:

o Try and build our own language processing engine using machine learning

§ Geared towards identifying topics that are related to meeting notes

§ Associate sentences with a person based on who is speaking, question v answer

§ Will be difficult…

o Use an API

§ Microsoft, Google, IBM all have NLP APIs

§ Returns entities, and categorizes these entities.

4. Filter through the entities

o Look for dates and deadlines

o Find the most important topics (ones that appear the most often, match preset topics)

o Construct a summary of the meeting

#### What we build:

· Python based, can be web-app

· Want to incorporate machine learning. Either in language processing (difficult), or trying to give speakers a role based on what they are talking about (seems unnecessary since you can pull info from Outlook)

· Ultimately build something that can generate meeting notes for you

If this needs to be more Genesys related, it can be used to summarize a call, though we have many similar tools (Speechminer, Pulse, Info Mart, Interactive Insights).


### How to run

Assuming python 3.6 or higher has been installed, we need to build a virtual dev environment using `virtualenv`. We can install `virtualenv` through `pip`:

```bash
$ pip install virtualenv
```

Then cd to root of the project and create a virtual environment:

```bash
$ virtualenv venv
```

We need to activate virtual environment before installing any dependencies:

```bash
$ source venv/bin/activate
```
*Note: if using Git Bash on Windows, the command could look like ```$ source venv/Scripts/activate```, it does the same thing.

Installing all the dependencies in `requirements.txt`:
```bash
$ pip install -r requirements.txt
```

Run the web app with this command:
```bash
$ python application.py
```

And we can access it by browsing `localhost:5000/`
