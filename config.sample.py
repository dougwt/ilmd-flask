import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

################
#  Sessions
################

SECRET_KEY = 'SecretKeyForSessionSigning'

################
#  Facebook API
################

FACEBOOK_APP_ID = 'XXXXXXXXXXXXXXX'
FACEBOOK_APP_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

################
# Database
################

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'ilmd.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

################
# Forms
################

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"
