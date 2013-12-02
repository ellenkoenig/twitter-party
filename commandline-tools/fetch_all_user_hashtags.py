#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import re

CONSUMER_KEY = os.environ['tw_pg_consumerkey']
CONSUMER_SECRET = os.environ['tw_pg_consumer']
OAUTH_TOKEN = os.environ['tw_pg_token']
OAUTH_TOKEN_SECRET = os.environ['tw_pg_secret']

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1', auth = auth, format = 'json')
posts = twitter_api.statuses.user_timeline(count = '200') #does not fetch retweeets right now, set included_rts = true if needed

pattern = re.compile('(?:\\s|\\A)[##]+([A-Za-z0-9-_]+)')
tweets = [ipost['text'] for ipost in posts] 

hashtags = []
for tweet in tweets:
	matcher = pattern.search(tweet)
	if(matcher is not None):
		hashtags.append(matcher.group())

print hashtags                   