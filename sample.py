import watson_developer_cloud
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions


from nltk import sent_tokenize
import nltk
import parsedatetime
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import requests
import json
from pprint import pprint

nltk.download('punkt', halt_on_error=False)

LANGUAGE="english"

class TranscriptAnalyzer:
	natural_language_understanding = NaturalLanguageUnderstandingV1(
		version='2017-02-27',
		username='db0edbd9-21f0-409e-8e45-d2ffa0d0630c',
		password='0ELgryFIquNn')
	def __init__(self, json_data):
		""" Input a transcript_file_path in the form of a string and a
			summary_number denoting the number of sentences requested in the summary.
		"""
		#self.sentence_blocks = "In tomorrow the rugged Colorado Desert of California, there lies buried a treasure ship sailed there hundreds of years ago by either Viking or Spanish explorers. Some say this is legend; others insist it is fact. A few have even claimed to have seen the ship, its wooden remains poking through the sand like the skeleton of a prehistoric beast. Among those who say they’ve come close to the ship is small-town librarian Myrtle Botts. In 1933, she was hiking with her husband in the Anza-Borrego Desert, not far from the border with Mexico. It was early March, so the desert would have been in bloom, its washed-out yellows and grays beaten back by the riotous invasion of wildflowers. Those wildflowers were what brought the Bottses to the desert, and they ended up near a tiny settlement called Agua Caliente. Surrounding place names reflected the strangeness and severity of the land: Moonlight Canyon, Hellhole Canyon, Indian Gorge. Try Newsweek for only $1.25 per week To enter the desert is to succumb to the unknowable. One morning, a prospector appeared in the couple’s camp with news far more astonishing than a new species of desert flora: He’d found a ship lodged in the rocky face of Canebrake Canyon. The vessel was made of wood, and there was a serpentine figure carved into its prow. There were also impressions on its flanks where shields had been attached—all the hallmarks of a Viking craft. Recounting the episode later, Botts said she and her husband saw the ship but couldn’t reach it, so they vowed to return the following day, better prepared for a rugged hike. That wasn’t to be, because, several hours later, there was a 6.4 magnitude earthquake in the waters off Huntington Beach, in Southern California. Botts claimed it dislodged rocks that buried her Viking ship, which she never saw again.There are reasons to doubt her story, yet it is only one of many about sightings of the desert ship. By the time Myrtle and her husband had set out to explore, amid the blooming poppies and evening primrose, the story of the lost desert ship was already about 60 years old. By the time I heard it, while working on a story about desert conservation, it had been nearly a century and a half since explorer Albert S. Evans had published the first account. Traveling to San Bernardino, Evans came into a valley that was “the grim and silent ghost of a dead sea,” presumably Lake Cahuilla. “The moon threw a track of shimmering light,” he wrote, directly upon “the wreck of a gallant ship, which may have gone down there centuries ago.” The route Evans took came nowhere near Canebrake Canyon, and the ship Evans claimed to see was Spanish, not Norse. Others have also seen this vessel, but much farther south, in Baja California, Mexico. Like all great legends, the desert ship is immune to its contradictions: It is fake news for the romantic soul, offering passage into some ancient American dreamtime when blood and gold were the main currencies of civic life.The legend does seem, prima facie, bonkers: a craft loaded with untold riches, sailed by early-European explorers into a vast lake that once stretched over much of inland Southern California, then run aground, abandoned by its crew and covered over by centuries of sand and rock and creosote bush as that lake dried out…and now it lies a few feet below the surface, in sight of the chicken-wire fence at the back of the Desert Dunes motel, $58 a night and HBO in most rooms.Totally insane, right? Let us slink back to our cubicles and never speak of the desert ship again. Let us only believe that which is shared with us on Facebook. Let us banish forever all traces of wonder from our lives. Yet there are believers who insist that, using recent advances in archaeology, the ship can be found. They point, for example, to a wooden sloop from the 1770s unearthed during excavations at the World Trade Center site in lower Manhattan, or the more than 40 ships, dating back perhaps 800 years, discovered in the Black Sea earlier this year."
		self.sentence_blocks = ""
		self.i = 0
		for result in json_data['results']:
			self.sentence_blocks += " " + result['alternatives'][0]['transcript']
			self.i = self.i+1
		self.schedule_words = [" piano "]#" by ", " due ", "plan", "setup", "schedule", "complete by", "complete on", "next", " on ", " in "]
		self.prohibited_schedule_words = ["today"]
		self.tokenized_transcript = sent_tokenize(self.sentence_blocks);
		parser = PlaintextParser.from_string(self.sentence_blocks, Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)

		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words(LANGUAGE)
		self.summary = summarizer(parser.document, self.i)

	def _get_things (self, sentence):
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
					topics+= [entity.get("text")]
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

url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
auth = ('914c12e3-abe4-4763-95a9-0fd97120d043', 'YSM7q8n6cXiC')
headers = {'Content-Type': 'audio/mp3'}
files = {'data-binary': open('./test.mp3', 'rb')}
params = {
	#'speaker_labels': 'true',
	'smart_formatting': 'true'
}

res = requests.post(url, auth=auth, headers=headers, files=files, params=params)

thing = TranscriptAnalyzer(res.json())
print (thing.frequently_discussed_topics())
print (thing.retrieve_calendar_items())
#{
#  "url": "https://stream.watsonplatform.net/speech-to-text/api",
#  "username": "914c12e3-abe4-4763-95a9-0fd97120d043",
#  "password": "YSM7q8n6cXiC"
#}

#{
#	"url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
#	"username": "db0edbd9-21f0-409e-8e45-d2ffa0d0630c",
#	"password": "0ELgryFIquNn"
#}