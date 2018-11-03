import json
import pprint
import pickle
import re

from adjustText import adjust_text
import matplotlib.pyplot as plt


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
	with open("C:\\Users\\werdn\\Documents\\GitHub\\USA REALLY\\usa-really-analysis\\posts-data.json", "r") as data:
		data = data.read()
		data = json.loads(data)
		for article in data["posts"]["data"]:
			score = get_rating(article["title"])
			titles.append(article["title"])
			scores.append(score)
			views.append(article["meta"]["post_views"])
		plot_data(views, scores, titles)
			# print('{0}\t{1}\t{2}'.format(article["title"], score, article["meta"]["post_views"]))


# classifier.show_most_informative_features(10)

def plot_data(x, y, labels):
	fig, ax = plt.subplots()
	ax.scatter(x, y)

	# for i, txt in enumerate(labels):
		# ax.annotate(txt, (x[i], y[i]))
	texts = [plt.text(x[i], y[i], labels[i], ha='center', va='center') for i in range(len(x))]
	# adjust_text(texts)
	# adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))   # super slow
	plt.xlabel("Pageview Count")
	plt.ylabel("Article Title Sentiment Score (+/-)")
	plt.show()



def plot_date_pageviews():
	with open("C:\\Users\\werdn\\Documents\\GitHub\\USA REALLY\\usa-really-analysis\\posts-data.json", "r") as data:
		data = data.read()
		data = json.loads(data)
		print(len(data))


read_saved_data()
