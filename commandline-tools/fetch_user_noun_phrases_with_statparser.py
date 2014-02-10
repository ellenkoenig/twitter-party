#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import nltk
import re
import pprint
from stat_parser import Parser  #just copy folder into site-packages

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
#
# stat_parser does all for steps above within its parser.
# TODO still need to check the results if they are reasonable.

parser = Parser()
result = [parser.parse(tweet) for tweet in tweets]

for res in result:
    print(res)

