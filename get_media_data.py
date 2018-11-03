import requests
import json
import pprint
import math
import time


"""
This file is designed to get ALL of the articles that exist on USA Really's site.
It saves this information into a JSON file in the same directory.
TODO: run requests asynchronously
"""

headers = {
	'Pragma': 'no-cache',
	'DNT': '1',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9,de;q=0.8,es;q=0.7',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
	'Accept': 'application/json, text/plain, */*',
	'Cache-Control': 'no-cache',
	'X-Requested-With': 'XMLHttpRequest',
	'Connection': 'keep-alive',
	'Referer': 'https://usareally.com/news',
}


def get_last_page_url():
	params = (
		('limit', '1'),
		('needParam', '1'),
		('page', '1'),
	)
	response = requests.get('https://usareally.com/posts/get', headers=headers, params=params)
	return json.loads(response.text)["posts"]["total"]


def get_data_from_page_number(num):
	params = (
		('limit', '50'),
		('needParam', '1'),
		('page', num),
	)
	print("getting data for page no. {0}...".format(num))
	response = requests.get('https://usareally.com/posts/get', headers=headers, params=params)
	data = json.loads(response.text)["posts"]["data"]
	return data


def save_data_to_file(data):
	filename = "usa-wow-full-data--{0}.json".format(time.strftime("%Y%m%d-%H%M%S"))
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)



last_page_num = math.ceil(get_last_page_url()/50)

full_data = []
for i in range(1, last_page_num+1):
	full_data.extend(get_data_from_page_number(i))

save_data_to_file(full_data)

print("retrieved", len(full_data), "articles")
