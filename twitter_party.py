from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_oauth import OAuth
import os

app = Flask(__name__)
app.secret_key="tw-party-gen"

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
    if session.has_key('twitter_token'):
        del session['twitter_token']
    next = url_for("success")
    callback = url_for('oauth_authorized', next = next)    
    return twitter.authorize(callback=callback)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    print resp
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
    render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
