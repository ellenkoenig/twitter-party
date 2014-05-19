#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
# uses the ems library found at http://pythonism.wordpress.com/2013/06/16/elementary-sentiment-analysis-on-a-text-using-python/, 
# also based on the source code listed there
          
import twitter
import os
import ems 
import pprint
import nltk

def analyze_tweet(tweet):
    emotion_words=[]
    for word in ems.em: #em being the dictionary of emotions imported via import em
    	if word in tweet:
    		emotion_words.append(ems.em[word])
    return emotion_words

def identify_emotions(tweets):
	emotions_in_all_tweets = []
	for tweet in tweets:
		tweet_emotions = analyze_tweet(tweet)
		if tweet_emotions:
			emotions_in_all_tweets += tweet_emotions 

	emotion_frequencies = nltk.FreqDist(emotions_in_all_tweets)
	return emotion_frequencies