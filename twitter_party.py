from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_oauth import OAuth
import os
import twitter
from fetch_matching_twitter_users import TwitterBot #fetch_user_location, fetch_user_keywords_and_hashtags, fetch_search_results, fetch_user_tweets
from compute_user_emotions import identify_emotions, filter_search_with_sentiment

app = Flask(__name__)
app.secret_key="tw-party-gen"

CONSUMER_KEY = os.environ['tw_pg_consumerkey'] 
CONSUMER_SECRET = os.environ['tw_pg_consumer']

oauth = OAuth()
twitter_oauth = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    session['params'] = request.form
    if session.has_key('twitter_token'):
        del session['twitter_token']
    next = url_for("success")
    callback = url_for('oauth_authorized', next = next)    
    return twitter_oauth.authorize(callback=callback)

@twitter_oauth.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/oauth-authorized')
@twitter_oauth.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

@app.route("/success")
def success():
    auth = twitter.oauth.OAuth(session['twitter_token'][0], session['twitter_token'][1], CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1', auth = auth, format = 'json')
    twitter_bot = TwitterBot(twitter_api, './nltk_data/', session['params']['no_of_keywords'], session['params']['location_radius'], session['params']['no_of_tweets_from_user_timeline'], session['params']['include_rts_in_timeline'], session['params']['no_of_search_results'])

    user_location = twitter_bot.fetch_user_location()
    (user_keywords, user_hashtags, keyword_freq) = twitter_bot.fetch_user_keywords_and_hashtags()
    hashtags = ", ".join(user_hashtags)

    user_tweets = twitter_bot.fetch_user_tweets()

    search_result_tweets = twitter_bot.fetch_search_results(user_location, user_keywords, user_hashtags)
    results_texts = [tweet['text'] for tweet in search_result_tweets]   

    if(session['params']['perform_sentiment_analysis']== u'yes'):
        user_emotions_with_frequencies = identify_emotions(user_tweets)
        user_emotions = ", ".join(user_emotions_with_frequencies.keys())

        party_emotions_with_frequencies = identify_emotions(results_texts)
        party_emotions = ", ".join(party_emotions_with_frequencies.keys())
        sentiment_matched_tweets = filter_search_with_sentiment(search_result_tweets, user_emotions_with_frequencies.keys())
        return render_template("success_and_party.html", location = user_location, result_tweets = sentiment_matched_tweets, keywords = user_keywords, kw_freq = keyword_freq, hashtags = hashtags, user_emotions = user_emotions, party_emotions = party_emotions)
    else:
        return render_template("success_and_party.html", location = user_location, result_tweets = search_result_tweets, keywords = user_keywords, kw_freq = keyword_freq, hashtags = hashtags, user_emotions = None, party_emotions = None)

if __name__ == "__main__":
    app.run(debug=True)
