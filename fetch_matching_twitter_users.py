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

		word_frequencies = nltk.FreqDist(stemmed_words)
		most_frequent_words = word_frequencies.keys()
		stopwords = set(nltk.corpus.stopwords.words('english'))
		most_frequent_words_without_stopwords  = [word for word in most_frequent_words if (word.lower() not in stopwords) and (word[:1] not in '@#' and len(word) > 3)]
		return most_frequent_words_without_stopwords[:self.no_of_keywords]

	def escape_unicode_chars(self, words):
		return [word.encode('unicode_escape') for word in words]

	def remove_special_chars(self, words):
		return [re.sub("[&%;]", "", word) for word in words]

	def clean_characters(self, words):
		return self.remove_special_chars(self.escape_unicode_chars(words))

	def fetch_user_tweets(self):
		posts = self.twitter_api.statuses.user_timeline(count = self.no_of_tweets_from_user_timeline, included_rts = self.include_rts_in_timeline) 
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
		return (self.escape_unicode_chars(self.clean_word_list(words)), self.clean_characters(hashtags))

	def fetch_search_results(self, location, keywords, hashtags):	
		keywords_and_hashtags = set(hashtags).union(set(keywords))
		query_string = urllib.quote_plus(" OR ".join(keywords_and_hashtags))
		search_results = self.twitter_api.search.tweets(q = query_string, geocode = location + ',' + self.location_radius, count = self.no_of_search_results)
		return search_results['statuses']