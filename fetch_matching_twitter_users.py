#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import re
import nltk
import urllib
import requests

#parameters
nltk.data.path.append('./nltk_data/')
no_of_keywords = 15
location_radius = "25km"
no_of_tweets_from_user_timeline = 200
include_rts_in_timeline = 'false'
no_of_search_results = 500

def convert_city_name_to_coordinates(city):
	request = requests.get('http://nominatim.openstreetmap.org/search?q=' + city + '&format=json')
	json = request.json()
	latitude =  json[0]['lat']
	longitude = json[0]['lon']
	return [latitude, longitude]

def fetch_user_location(twitter_api):
	profile = twitter_api.account.verify_credentials()
	coords = convert_city_name_to_coordinates(profile['location'])
	return ",".join(coords)

def clean_word_list(words):
	cleaned_words = clean_characters(words)
	myPorterStemmer = nltk.stem.porter.PorterStemmer()
	stemmed_words = [myPorterStemmer.stem(word) for word in cleaned_words]

	word_frequencies = nltk.FreqDist(stemmed_words)
	most_frequent_words = word_frequencies.keys()
	stopwords = set(nltk.corpus.stopwords.words('english'))
	most_frequent_words_without_stopwords  = [word for word in most_frequent_words if (word.lower() not in stopwords) and (word[:1] not in '@#' and len(word) > 3)]
	return most_frequent_words_without_stopwords[:no_of_keywords]

def escape_unicode_chars(words):
	return [word.encode('unicode_escape') for word in words]

def remove_special_chars(words):
	return [re.sub("[&%;]", "", word) for word in words]

def clean_characters(words):
	return remove_special_chars(escape_unicode_chars(words))

def fetch_user_tweets(twitter_api):
	posts = twitter_api.statuses.user_timeline(count = no_of_tweets_from_user_timeline, included_rts = include_rts_in_timeline) 
	return [post['text'] for post in posts]

def fetch_user_keywords_and_hashtags(twitter_api):
	tweets = fetch_user_tweets(twitter_api) 

	pattern = re.compile('(?:\\s|\\A)[##]+([A-Za-z0-9-_]+)')
	hashtags = []
	words = []

	for tweet in tweets:
		matcher = pattern.search(tweet)
		if(matcher is not None):
			hashtags.append("#" + matcher.group(1))
		words += tweet.split() #this builds the word list for identifying the key words, not relevant to hashtag search
	return (escape_unicode_chars(clean_word_list(words)), clean_characters(hashtags))

def fetch_search_results(twitter_api, location, keywords, hashtags):	
	keywords_and_hashtags = set(hashtags).union(set(keywords))
	query_string = urllib.quote_plus(" OR ".join(keywords_and_hashtags))
	search_results = twitter_api.search.tweets(q = query_string, geocode = location + ',' + location_radius, count = no_of_search_results)
	return search_results['statuses']