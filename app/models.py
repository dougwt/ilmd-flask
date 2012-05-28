from flask import render_template, url_for
from app import db
# from gallery import resize_image
import datetime
from PIL import Image as PILimage


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    hidden = db.Column(db.Boolean)
    images = db.relationship('Image', backref='category', lazy='dynamic')

    def __init__(self, name=None, hidden=False):
        self.name = name
        self.hidden = hidden

    def __repr__(self):
        return '<Category %s: %r' % (self.id, self.name)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    caption = db.Column(db.String(300))
    angelpup = db.Column(db.Boolean)
    filetype = db.Column(db.Enum('.jpg', '.png'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    hidden = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, caption, angelpup=False, filetype='.jpg', category_id=1, hidden=False):
        self.name = name
        self.caption = caption
        self.angelpup = angelpup
        self.filetype = filetype
        self.category_id = category_id
        self.hidden = hidden

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
