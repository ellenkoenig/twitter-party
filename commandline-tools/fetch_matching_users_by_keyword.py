#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import nltk
import urllib

CONSUMER_KEY = os.environ['tw_pg_consumerkey']
CONSUMER_SECRET = os.environ['tw_pg_consumer']
OAUTH_TOKEN = os.environ['tw_pg_token']
OAUTH_TOKEN_SECRET = os.environ['tw_pg_secret']

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1', auth = auth, format = 'json')
posts = twitter_api.statuses.user_timeline(count = '200') #does not fetch retweeets right now, set included_rts = true if needed

# pull out tweets as list
tweets = [ipost['text'] for ipost in posts] 
words = []
for tweet in tweets:
	words += tweet.split()

myPorterStemmer = nltk.stem.porter.PorterStemmer()
stemmed_words = [myPorterStemmer.stem(word) for word in words]

word_frequencies = nltk.FreqDist(stemmed_words)
most_frequent_words = word_frequencies.keys()
stopwords =  set(nltk.corpus.stopwords.words('english'))
most_frequent_words_without_stopwords  = [word for word in most_frequent_words if (word.lower() not in stopwords) and (word[:1] not in '@#' and len(word) > 3)]

query_string = urllib.quote_plus(" OR ".join(most_frequent_words_without_stopwords[:10]))
print query_string
search_results = twitter_api.search.tweets(q = query_string, count = 100)

for status in search_results['statuses']:
	print status['text']
	print status['user']['name']

