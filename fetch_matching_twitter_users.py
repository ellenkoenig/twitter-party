#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import re
import nltk
import urllib
import requests

#parameters
class TwitterBot(object):

	def __init__(self, twitter_api, nltk_data_path = './nltk_data/', no_of_keywords = 15, location_radius = "25km", no_of_tweets_from_user_timeline = 100, include_rts_in_timeline = 'false', no_of_search_results = 100):
		nltk.data.path.append(nltk_data_path)
		self.twitter_api = twitter_api
		self.no_of_keywords = int(no_of_keywords)
		self.location_radius = location_radius
		self.no_of_tweets_from_user_timeline = int(no_of_tweets_from_user_timeline)
		self.include_rts_in_timeline = (include_rts_in_timeline== u'yes')
		self.no_of_search_results = int(no_of_search_results)

	def convert_city_name_to_coordinates(self, city):
		request = requests.get('http://nominatim.openstreetmap.org/search?q=' + city + '&format=json')
		json = request.json()
		latitude =  json[0]['lat']
		longitude = json[0]['lon']
		return [latitude, longitude]

	def fetch_user_location(self):
		profile = self.twitter_api.account.verify_credentials()
		coords = self.convert_city_name_to_coordinates(profile['location'])
		return ",".join(coords)

	def clean_word_list(self, words):
		cleaned_words = self.clean_characters(words)
		myPorterStemmer = nltk.stem.porter.PorterStemmer()
		stemmed_words = [myPorterStemmer.stem(word) for word in cleaned_words]

		stopwords = set(nltk.corpus.stopwords.words('english'))
		words_without_stopwords  = [word for word in cleaned_words if (word.lower() not in stopwords) and (word[:1] not in '@#' and word[:4] != 'http' and len(word) > 3)]

		myPorterStemmer = nltk.stem.porter.PorterStemmer()
		stemmed_words = [myPorterStemmer.stem(word) for word in words_without_stopwords]

		word_frequencies = nltk.FreqDist(stemmed_words)
		most_frequent_words = word_frequencies.keys()[:self.no_of_keywords]
		frequencies = [word_frequencies[word] for word in most_frequent_words]
		# normalize frequency values so largest value is 300 and lowest 100
		max_freq = max(frequencies)
		min_freq = min(frequencies)
		max_val = 300
		min_val = 100
		norm_freq = [(freq-min_freq)/(max_freq-min_freq)*(max_val - min_val) + min_val for freq in frequencies]
		return dict(zip(most_frequent_words,norm_freq))

	def escape_unicode_chars(self, words):
		return [word.encode('unicode_escape') for word in words]

	def remove_special_chars(self, words):
		return [re.sub("[&%;:\(\)!\.,\?\+\*-=]", "", word) for word in words]

	def clean_characters(self, words):
		return self.remove_special_chars(self.escape_unicode_chars(words))

	def fetch_user_tweets(self):
		posts = self.twitter_api.statuses.user_timeline(count = self.no_of_tweets_from_user_timeline, included_rts = self.include_rts_in_timeline) 
		while(len(posts) < self.no_of_tweets_from_user_timeline): #we need to fetch more pages to reach the no that the user requested
			ids = [int(post["id"]) for post in posts]
			max_id = max(ids) - 1
			posts += self.twitter_api.statuses.user_timeline(count = self.no_of_tweets_from_user_timeline, included_rts = self.include_rts_in_timeline, max_id = max_id)			

		return [post['text'] for post in posts]

	def fetch_user_keywords_and_hashtags(self):
		tweets = self.fetch_user_tweets() 

		pattern = re.compile('(?:\\s|\\A)[##]+([A-Za-z0-9-_]+)')
		hashtags = []
		words = []

		for tweet in tweets:
			matcher = pattern.search(tweet)
			if(matcher is not None):
				hashtags.append("#" + matcher.group(1))
			words += tweet.split() #this builds the word list for identifying the key words, not relevant to hashtag search
		dict_words_freq = self.clean_word_list(words)
		return (self.escape_unicode_chars(dict_words_freq.keys()), self.clean_characters(hashtags),dict_words_freq)

	def fetch_search_results(self, location, keywords, hashtags):	
		keywords_and_hashtags = set(hashtags).union(set(keywords))
		query_string = urllib.quote_plus(" OR ".join(keywords_and_hashtags))
		search_results = self.twitter_api.search.tweets(q = query_string, geocode = location + ',' + self.location_radius, count = self.no_of_search_results)
		statuses = search_results['statuses']
		while(len(statuses) < self.no_of_search_results): #we need to fetch more pages to reach the no that the user requested
			ids = [int(status['id']) for status in statuses]
			max_id = max(ids) - 1
			results = self.twitter_api.search.tweets(q = query_string, geocode = location + ',' + self.location_radius, count = self.no_of_search_results, max_id = max_id)			
			statuses += results['statuses']

		return statuses
