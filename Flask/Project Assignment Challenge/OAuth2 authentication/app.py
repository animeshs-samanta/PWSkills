from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure OAuth for Google
oauth_google = OAuth(app)
google = oauth_google.remote_app(
    'google',
    consumer_key='your_google_client_id',
    consumer_secret='your_google_client_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Configure OAuth for Facebook
oauth_facebook = OAuth(app)
facebook = oauth_facebook.remote_app(
    'facebook',
    consumer_key='your_facebook_app_id',
    consumer_secret='your_facebook_app_secret',
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
)

# Callback routes for Google and Facebook
@app.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('authorized_google', _external=True))

@app.route('/login/facebook')
def login_facebook():
    return facebook.authorize(callback=url_for('authorized_facebook', _external=True))

# Callback method for Google
@app.route('/login/google/authorized')
def authorized_google():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    # Here you can use user_info to get user details from Google
    return 'Logged in as: ' + user_info.data['email']

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# Callback method for Facebook
@app.route('/login/facebook/authorized')
def authorized_facebook():
    response = facebook.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['facebook_token'] = (response['access_token'], '')
    user_info = facebook.get('/me?fields=id,email')
    # Here you can use user_info to get user details from Facebook
    return 'Logged in as: ' + user_info.data['email']

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')

# Logout route
@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('facebook_token', None)
    return 'Logged out'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
