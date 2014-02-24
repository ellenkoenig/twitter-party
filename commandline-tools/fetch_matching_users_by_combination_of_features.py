#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import re
import nltk
import urllib
import requests

#parameters
no_of_keywords = 15
location_radius = "25km"
no_of_tweets_from_user_timeline = 200
include_rts_in_timeline = 'false'
no_of_search_results = 100

def initiate_twitter_api():
	CONSUMER_KEY = os.environ['tw_pg_consumerkey']
	CONSUMER_SECRET = os.environ['tw_pg_consumer']
	OAUTH_TOKEN = os.environ['tw_pg_token']
	OAUTH_TOKEN_SECRET = os.environ['tw_pg_secret']

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	return twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1', auth = auth, format = 'json')

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
	myPorterStemmer = nltk.stem.porter.PorterStemmer()
	stemmed_words = [myPorterStemmer.stem(word) for word in words]

	word_frequencies = nltk.FreqDist(stemmed_words)
	most_frequent_words = word_frequencies.keys()
	stopwords =  set(nltk.corpus.stopwords.words('english'))
	most_frequent_words_without_stopwords  = [word for word in most_frequent_words if (word.lower() not in stopwords) and (word[:1] not in '@#' and len(word) > 3)]
	return most_frequent_words_without_stopwords[:no_of_keywords]


def fetch_user_keywords_and_hashtags(twitter_api):
	posts = twitter_api.statuses.user_timeline(count = no_of_tweets_from_user_timeline, included_rts = include_rts_in_timeline) 
	tweets = [ipost['text'] for ipost in posts] 

	pattern = re.compile('(?:\\s|\\A)[##]+([A-Za-z0-9-_]+)')
	hashtags = []
	words = []

	for tweet in tweets:
		matcher = pattern.search(tweet)
		if(matcher is not None):
			hashtags.append("#" + matcher.group(1))
		words += tweet.split()

	return (clean_word_list(words), hashtags)

def fetch_search_results(twitter_api, location, keywords, hashtags):	
	keywords_and_hashtags = set(hashtags).union(set(keywords))
	query_string = urllib.quote_plus(" OR ".join(keywords_and_hashtags))
	search_results = twitter_api.search.tweets(q = query_string, geocode = location + ',' + location_radius, count = no_of_search_results)
	return search_results['statuses']


twitter_api = initiate_twitter_api()
location = fetch_user_location(twitter_api)
(keywords, hashtags) = fetch_user_keywords_and_hashtags(twitter_api)
search_result_tweets = fetch_search_results(twitter_api, location, keywords, hashtags)

for result in search_result_tweets:
		print result['text']
		print result['user']['name']

