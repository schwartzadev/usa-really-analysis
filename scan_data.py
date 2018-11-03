import json
import pprint
import pickle
import re

from adjustText import adjust_text
import matplotlib.pyplot as plt
import matplotlib
import datetime
import numpy as np
from html.parser import HTMLParser

plt.rcParams['font.sans-serif'] = ['Helvetica']


NEWS_DATA_FILE = 'C:\\Users\\werdn\\Documents\\GitHub\\USA REALLY\\usa-really-analysis\\usa-wow-full-data--20181102-180155.json'

def sentence_list(sentence):
	return re.sub("[^\w]", " ",  sentence).split()

def sentence_features(sentence, isList=False):
	if not isList:
		sentence_words = sentence_list(sentence)
	else:
		sentence_words = sentence
	features = {}
	for word in sentence_words:
		features['contains({})'.format(word)] = (word in sentence_words)
	return features


def load_model():
	f = open('C:\\Users\\werdn\\Documents\\GitHub\\USA REALLY\\Sentiment-Analysis-NLTK\\twitter_classifier.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()
	print("Model loaded")
	return classifier


class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs= True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def clean_content(raw_content):
	dirty_words = strip_tags(raw_content)
	cleaned_words = re.sub("[^\w]", " ",  dirty_words).split()
	return cleaned_words


classifier = load_model()


def get_rating(sentence, isList=False):
	neg = 0
	pos = 0
	result = classifier.classify(sentence_features(sentence, isList))
	if isList:
		sentence_length = len(sentence)
	else:
		sentence_length = len(sentence_list(sentence))
	score = 0
	if result == 'neg':
		neg = neg + 1
		score = neg*(-1)
	if result == 'pos':
		pos = pos + 1
		score = pos
	score = score/sentence_length
	# print(sentence)
	# print('    ', + score)
	return score


def sentiment_over_time(filename):
	"""
	Plots sentiment (y axis) and time (x axis).
	Uses an article's content to determine sentiment.
	"""
	y = []
	x = []
	with open(filename, "r") as data:
		data = json.loads(data.read())
		for article in data:
			score = get_rating(clean_content(article["content"]), True)
			y.append(score)
			x.append(article["published_at"])

	dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x]
	dates = matplotlib.dates.date2num(dates)

	fig, ax = plt.subplots()
	ax.set_ylim(-0.05, 0.05)
	ax.axhline(y=0, dashes=(10,10), color="grey")
	ax.plot_date(dates, y, alpha=0.4)
	ax.set_xlim([datetime.date(2018, 5, 20), datetime.datetime.now()])

	plt.title("Sentiment Over Time on USA Really Articles")
	plt.ylabel("Article Title Sentiment Score")
	plt.xlabel("Published Date")
	plt.show()



def sentiment_over_pageviews(filename):
	"""
	Plots sentiment (y axis) and number of article pageviews (x axis).
	Uses an article's content to determine sentiment.
	"""
	labels = []
	y = []
	x = []
	c = []
	with open(filename, "r") as data:
		data = json.loads(data.read())
		for article in data:
			score = get_rating(clean_content(article["content"]), True)
			labels.append(article["title"])
			y.append(score)
			x.append(article["meta"]["post_views"])
			c.append(article["meta"]["word_cnt"])  # color based on word count

	fig, ax = plt.subplots()
	ax.set_facecolor((0, 0, 0, .3))
	ax.scatter(x, y, c=c, cmap='Blues', s=20, alpha=0.4)
	# ax.scatter(x, y, s=20, facecolors='r', edgecolors='r', alpha=0.2)

	# texts = [plt.text(x[i], y[i], labels[i], ha='center', va='center') for i in range(len(x))]
	ax.set_xscale('log')
	ax.set_ylim(-0.05, 0.05)
	ax.axhline(y=0, dashes=(10,10), color="white")
	# adjust_text(texts)
	# adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))   # super slow
	plt.title("Pageviews vs. Sentiment on USA Really Articles")
	plt.xlabel("Pageview Count (logarithmic scale)")
	plt.ylabel("Article Title Sentiment Score")
	plt.show()


def plot_date_pageviews(filename):
	"""
	Plots pageviews per article over time for USA Really's posts
	"""
	with open(filename, "r") as data:
		data = data.read()
		data = json.loads(data)
		x = []
		y = []
		for article in data:
			x.append(article["published_at"])
			y.append(article["meta"]["post_views"])
		fig, ax = plt.subplots()
		dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x]
		dates = matplotlib.dates.date2num(dates)
		ax.plot_date(dates, y)
		ax.set_yscale('log')
		plt.title("USA Really Post Views Over Time")
		plt.xlabel("Publishing Date")
		plt.ylabel("Post Views")
		plt.show()


plot_date_pageviews(NEWS_DATA_FILE)
