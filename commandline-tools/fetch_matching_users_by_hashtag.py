#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
          
import twitter
import os
import re
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
pattern = re.compile('(?:\\s|\\A)[##]+([A-Za-z0-9-_]+)')

hashtags = []
for tweet in tweets:
	matcher = pattern.search(tweet)
	if(matcher is not None):
		hashtags.append("#" + matcher.group(1))
               
query_string = urllib.quote_plus(" OR ".join(set(hashtags)))
search_results = twitter_api.search.tweets(q = query_string, count = 100)

for status in search_results['statuses']:
	print status['text']
	print status['user']['name']