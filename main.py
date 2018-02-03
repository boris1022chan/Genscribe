import watson_developer_cloud
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, \
    ConceptsOptions, CategoriesOptions

import nltk
# import nltk.tokenize.punkt
nltk.data.path.append("/usr/local/share/nltk_data/nltk_data")
nltk.data.path.append("../usr/local/share/nltk_data")
nltk.data.path.append("/usr/local/share/nltk_data/tokenizers/punkt/py3")
nltk.data.path.append("../usr/local/share/nltk_data/tokenizers/punkt/py3")

from nltk import sent_tokenize
import parsedatetime
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import requests
#
# nltk.download('punkt')

LANGUAGE = "english"

class myClass:
    def __init__(self):
        return

    def _out(self):
        return "my class output 3.5"


def _output():
    return "Hello World"

class TranscriptAnalyzer:
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2017-02-27',
        username='db0edbd9-21f0-409e-8e45-d2ffa0d0630c',
        password='0ELgryFIquNn')

    def __init__(self, path, type):
        """ Input a transcript_file_path in the form of a string and a
			summary_number denoting the number of sentences requested in the summary.
		"""

        url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
        auth = ('914c12e3-abe4-4763-95a9-0fd97120d043', 'YSM7q8n6cXiC')
        headers = {'Content-Type': type}
        # files = {'data-binary': open(path, 'rb')}
        files = {'data-binary': path}
        params = {
            # 'speaker_labels': 'true',
            'smart_formatting': 'true'
        }

        res = requests.post(url, auth=auth, headers=headers, files=files, params=params)

        self.sentence_blocks = ""
        self.i = 0
        json_data = res.json()
        for result in json_data['results']:
            self.sentence_blocks += " " + result['alternatives'][0]['transcript']
            self.i = self.i + 1
        self.schedule_words = [" by ", " due ", "plan", "setup", "schedule", "complete by", "complete on", "next",
                               " on ", " in "]
        self.prohibited_schedule_words = ["today"]
        self.tokenized_transcript = sent_tokenize(self.sentence_blocks);
        parser = PlaintextParser.from_string(self.sentence_blocks, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        self.summary = summarizer(parser.document, self.i)

    def _get_things(self, sentence):
        try:
            response = self.natural_language_understanding.analyze(
                text=sentence,
                features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()))
            # Returns a set of the most frequently discussed topics
            topics = []
            for keyword in response.get("keywords"):
                if keyword.get("text") is not None:
                    topics += [keyword.get("text")];
            for entity in response.get("entities"):
                if entity.get("text") is not None:
                    topics += [entity.get("text")]
            return topics
        except watson_developer_cloud.watson_service.WatsonApiException:
            return []

    def _date_parser(self, sentence):
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(sentence)
        time_struct_null, parse_status_null = cal.parse("")

        # If the time detected is the same as the current time, discard.
        if datetime(*time_struct[:6]) == datetime(*time_struct_null[:6]):
            return None
        # For ease of use, events cannot be scheduled for the same day with use of the word "today."
        # A relative term ("in an hour") should be used instead.
        for word in self.prohibited_schedule_words:
            if word in sentence:
                return None

        for word in self.schedule_words:
            if word in sentence:
                return datetime(*time_struct[:6])
        return None

    def frequently_discussed_topics(self):
        # Returns a set of the most frequently discussed topics
        topics = []
        for sentence in self.summary:
            topics += self._get_things(str(sentence))
        numImportantTopics = self.i / 5
        important_topics = []
        for item in topics:
            if topics.count(item) >= numImportantTopics:
                important_topics += [item]
        return important_topics

    def retrieve_calendar_items(self):
        # Returns a tuple containing the context or sentence defining the event,
        # a datetime.datetime date and a list of keywords relevant to the event.
        calendar_items = []
        for sentence in self.tokenized_transcript:
            possible_date = self._date_parser(sentence)
            if possible_date is not None:
                calendar_items += [(sentence, possible_date, self._get_things(sentence))]
        return calendar_items
