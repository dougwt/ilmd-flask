from flask import url_for, session, request, redirect, flash
from app import facebook, db, models


def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


def logout():
    session.pop('facebook_id', None)
    session.pop('oauth_token', None)
    return redirect(url_for('home'))


@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    flash('Welcome back, %s' % me.data['name'])
    next = request.args.get('next')
    store_user(me.data, resp['access_token'])
    session['facebook_id'] = me.data['id']
    return redirect(next)
    # return "Logged in as id='%s' sess_id='%s' name='%s' email='%s' redirect='%s'" % \
    #     (me.data['id'], session['facebook_id'], me.data['name'], me.data['email'], next)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


def store_user(profile, access_token):
    facebook_id = int(profile['id'])
    name = profile['name']
    email = profile['email']
    # user = models.User.get_by_key_name(cookie["uid"])
    user = models.User.get_facebook_id(facebook_id)
    if user:
        user.name = name
        user.email = email
        user.access_token = access_token
    else:
        user = models.User(facebook_id=facebook_id,
                           name=name,
                           email=email,
                           description=None,
                           access_token=access_token,
                           role='admin')
        db.session.add(user)
    db.session.commit()
