from flask import Flask, render_template, request, session, url_for, redirect
from flask_oauth import OAuth
import os
import logging

app = Flask(__name__)

CONSUMER_KEY = os.environ['tw_pg_consumerkey'] 
CONSUMER_SECRET = os.environ['tw_pg_consumer'] 

oauth = OAuth()
twitter = oauth.remote_app('twitter',
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

@app.route('/login')
def login():
    print("Hello, World!")
    app.logger.info("Started login method")
    session['next'] = request.args.get('next') or request.referrer or None
    app.logger.info(session['next'])
    callback = url_for('oauth_authorized')   
    app.logger.info(callback) 
    return render_template('index.html') #twitter.authorize(callback=callback, next = session['next'])


@app.route('/results', methods = ['POST'])
def results():
	handle = request.form['handle']
	return render_template('results.html', token = token)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/oauth-authorized')
@twitter.authorized_handler
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

if __name__ == "__main__":
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
