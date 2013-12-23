#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import nltk

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

word_frequencies = nltk.FreqDist(words)
most_frequent_words = word_frequencies.keys()
stopwords =  set(nltk.corpus.stopwords.words('english'))
most_frequent_words_without_stopwords  = [word for word in most_frequent_words if word.lower() not in stopwords]
print most_frequent_words_without_stopwords[:25]