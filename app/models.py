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

    def __repr__(self):
        return '<Category %s: %r' % (self.id, self.name)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    filetype = db.Column(db.Enum('.jpg', '.png'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    hidden = db.Column(db.Boolean, default=True)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    likes = db.relationship('Like', backref='image', lazy='dynamic')
    tags = db.relationship('Tag', backref='image', lazy='dynamic')

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


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300))
    angelpup = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', backref='pet', lazy='dynamic')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(300))
    admin = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    pets = db.relationship('Pet', backref='user', lazy='dynamic')
