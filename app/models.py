from flask import render_template, url_for
from app import db
# from gallery import resize_image
import datetime
from PIL import Image as PILimage


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    hidden = db.Column(db.Boolean, default=False)
    images = db.relationship('Image', backref='category', lazy='dynamic')

    def __init__(self, name, hidden=False):
        self.name = name
        self.hidden = hidden

    def __repr__(self):
        return '<Category %s: %r' % (self.id, self.name)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.DateTime)

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
        self.date_added = datetime.datetime.utcnow()


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    filetype = db.Column(db.Enum('.jpg', '.png'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    hidden = db.Column(db.Boolean, default=True)
    date_added = db.Column(db.DateTime)
    likes = db.relationship('Like', backref='image', lazy='dynamic')
    tags = db.relationship('Tag', backref='image', lazy='dynamic')

    def __init__(self, description, filetype, category_id, hidden=True):
        self.description = description
        self.filetype = filetype
        self.category_id = category_id
        self.hidden = hidden
        self.date_added = datetime.datetime.utcnow()

    def __unicode__(self):
        return render_template('image.html', image=self)

    def __repr__(self):
        return '<Image %s: %r>' % (self.id, self.name)

    def generate_thumbnail(self, path='app/static/gallery/', width=128, height=128):
        original_filepath = path + str(self.id) + self.filetype
        new_filepath = path + str(self.id) + '.thumb' + self.filetype
        img = PILimage.open(original_filepath)
        # resize_image(img)
        img.thumbnail((width, height), PILimage.ANTIALIAS)
        img.save(new_filepath)


class ImageDemo():
    def __init__(self, id=1, name="Ashas", caption="This is a sample caption", angelpup=False):
        self.id = id
        self.name = name
        self.caption = caption
        self.filetype = '.jpg'
        self.angelpup = angelpup

    def __unicode__(self):
        return render_template('image.html', image=self)

    def permalink(self):
        return url_for('single', id=self.id)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, image_id, user_id):
        self.image_id = image_id
        self.user_id = user_id


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300))
    angelpup = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', backref='pet', lazy='dynamic')

    def __init__(self, name, description, angelpup, user_id):
        self.name = name
        self.description = description
        self.angelpup = angelpup
        self.user_id = user_id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def __init__(self, pet_id, image_id):
        self.pet_id = pet_id
        self.image_id = image_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(300))
    access_token = db.Column(db.String(300), unique=True, nullable=False)  # fb OAUTH access token
    role = db.Column(db.Enum('user', 'trusted', 'admin'))
    date_added = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    pets = db.relationship('Pet', backref='user', lazy='dynamic')

    # id = db.StringProperty(required=True) #facebook user-id
    # created = db.DateTimeProperty(auto_now_add=True)
    # updated = db.DateTimeProperty(auto_now=True)
    # name = db.StringProperty(required=True)
    # profile_url = db.StringProperty(required=True)
    # access_token = db.StringProperty(required=True)  #fb OAUTH access token

    def __init__(self, facebook_id, name, email, description, access_token, role='user'):
        self.facebook_id = facebook_id
        self.name = name
        self.email = email
        self.description = description
        self.access_token = access_token
        self.role = role
        self.date_added = datetime.datetime.utcnow()

    def trusted(self):
        return self.role is 'trusted' or self.role is 'admin'

    def admin(self):
        return self.role is 'admin'

    @staticmethod
    def get_facebook_id(facebook_id):
        return User.query.filter_by(facebook_id=facebook_id).first()
