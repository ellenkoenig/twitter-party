#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
#This is the version that works AND outputs python objects	! :D
          
import twitter
import os
import json

CONSUMER_KEY = os.environ['tw_pg_consumerkey']
CONSUMER_SECRET = os.environ['tw_pg_consumer']
OAUTH_TOKEN = os.environ['tw_pg_token']
OAUTH_TOKEN_SECRET = os.environ['tw_pg_secret']

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1', auth = auth, format = 'json')
posts = twitter_api.statuses.user_timeline(count = '200', include_rts = 'true') 

print json.dumps(posts, indent = 1)
	
                          