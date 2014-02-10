#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import twitter
import urllib
import requests

def convert_city_name_to_coordinates(city):
	request = requests.get('http://nominatim.openstreetmap.org/search?q=' + city + '&format=json')
	json = request.json()
	latitude =  json[0]['lat']
	longitude = json[0]['lon']
	return [latitude, longitude]


CONSUMER_KEY = os.environ['tw_pg_consumerkey']
CONSUMER_SECRET = os.environ['tw_pg_consumer']
OAUTH_TOKEN = os.environ['tw_pg_token']
OAUTH_TOKEN_SECRET = os.environ['tw_pg_secret']

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1', auth = auth, format = 'json')
profile = twitter_api.account.verify_credentials()
coords = convert_city_name_to_coordinates(profile['location'])

location = ",".join(coords)
query_string = urllib.quote_plus("a")
search_results = twitter_api.search.tweets(q = query_string, geocode = location + ',25km', count = 100)

for status in search_results['statuses']:
	if(status['coordinates'] is not None):
		print(status['coordinates'])
	else:
		print(status['user']['location'])
	print(status['user']['name'])

