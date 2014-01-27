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
search_results = twitter_api.search.tweets(q="hack", count= 1) #optional: geocode=XYZ
print search_results['statuses'][0]['text']
print search_results['statuses'][0]['user']['name']

