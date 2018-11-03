import json
import pprint
import pickle
import re

from adjustText import adjust_text
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import numpy as np


def sentence_list(sentence):
	return re.sub("[^\w]", " ",  sentence).split()	

def sentence_features(sentence):
	sentence_words = sentence_list(sentence)
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


classifier = load_model()

def get_rating(sentence):
	neg = 0
	pos = 0
	result = classifier.classify(sentence_features(sentence))
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

# https://usareally.com/posts/get?limit=1832&needParam=1

def read_saved_data():
	titles = []
	scores = []
	views = []
	with open("C:\\Users\\werdn\\Documents\\GitHub\\USA REALLY\\usa-really-analysis\\usa-wow-full-data--20181102-180155.json", "r") as data:
		data = data.read()
		data = json.loads(data)
		for article in data:
			score = get_rating(article["title"])
			titles.append(article["title"])
			scores.append(score)
			views.append(article["meta"]["post_views"])
		plot_scatterplot(views, scores, titles)


def plot_scatterplot(filename):
	labels = []
	y = []
	x = []
	with open(filename, "r") as data:
		data = json.loads(data.read())
		for article in data:
			score = get_rating(article["title"])
			labels.append(article["title"])
			y.append(score)
			x.append(article["meta"]["post_views"])

	fig, ax = plt.subplots()
	ax.scatter(x, y)

	# for i, txt in enumerate(labels):
		# ax.annotate(txt, (x[i], y[i]))

	# texts = [plt.text(x[i], y[i], labels[i], ha='center', va='center') for i in range(len(x))]
	ax.set_xscale('log')
	# adjust_text(texts)
	# adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))   # super slow
	plt.title("Pageviews vs. Sentiment on USA Really Articles")
	plt.xlabel("Pageview Count")
	plt.ylabel("Article Title Sentiment Score (logarithmic scale)")
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

		dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x]
		dates = matplotlib.dates.date2num(dates)
		ax.plot_date(dates, y)
		plt.title("USA Really Post Views Over Time")
		plt.xlabel("Publishing Date")
		plt.ylabel("Post Views")
		plt.show()
