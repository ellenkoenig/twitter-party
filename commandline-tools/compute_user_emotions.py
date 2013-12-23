#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
# uses the ems library found at http://pythonism.wordpress.com/2013/06/16/elementary-sentiment-analysis-on-a-text-using-python/, 
# also based on the source code listed there
          
import twitter
import os
import ems 
import pprint
import nltk

def fetch_tweets():
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
	return tweets

def analyze(sentence):
    emotion_words=[]
    for word in ems.em: #em being the dictionary of emotions imported via import em
        if word in sentence:
            emotion_words.append(ems.em[word])
    return emotion_words

tweets = fetch_tweets()

emotions_in_tweets = []
for tweet in tweets:
	tweet_emotion = analyze(tweet)
	if tweet_emotion:
		emotions_in_tweets += tweet_emotion 

emotion_frequencies = nltk.FreqDist(emotions_in_tweets)
print(emotion_frequencies)