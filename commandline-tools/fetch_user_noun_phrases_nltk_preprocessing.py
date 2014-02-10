#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import nltk
import re
import pprint

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

#####
# apply regexp chunker to get noun phrases
# http://nltk.org/book3/ch07.html
# process: 1) sentence segmentation, 2) tokenization, 3) part of speech tagging
# 4) entity detection
# first three tasks can be done with nltk functions
#
# need to manually download:
# - punkt (Punkt Tokenizer Models)
# - maxent_treebank_pos_tagger(Treebank Part of Speech Tagger(Maximum entropy))

def ie_preprocess(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

tweets_preproc = [ie_preprocess(tweet) for tweet in tweets]

# TODO use more complicated grammar
#grammar = "NP: {<DT>? <JJ>* <NN>*}"
#cp = nltk.RegexpParser(grammar)
#result = [cp.parse(sent) for sent in tweets_preproc[0]]

#print(result)
