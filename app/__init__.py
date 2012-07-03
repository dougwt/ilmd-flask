from flask import Flask, session, render_template
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.oauth import OAuth

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


class View(MethodView):
    def current_user(self):
        if 'facebook_id' in session:
            facebook_id = session['facebook_id']
            return models.User.get_facebook_id(facebook_id)


from app import urls, models
