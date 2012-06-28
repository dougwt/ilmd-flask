from flask import Flask
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


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404


class View(MethodView):
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            FACEBOOK_APP_ID = app.config['FACEBOOK_APP_ID']
            FACEBOOK_APP_SECRET = app.config['FACEBOOK_APP_SECRET']
            cookie = facebook.get_user_from_cookie(
                self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                user = models.User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = models.User(facebook_id=int(profile["id"]),
                                       name=profile["name"],
                                       profile_url=profile["link"],
                                       access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        return self._current_user


from app import urls, models
