from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, url_for

db = SQLAlchemy()


class Category(db.Model):
    # id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    hidden = db.Column(db.Boolean)

    def __init__(self, name=None, hidden=False):
        self.name = name
        self.hidden = hidden

    def __repr__(self):
        return '<Category: %s' % (self.name)


class Image(db.Model):
    # FILETYPE_CHOICES = (
    #     ('J', '.jpg'),
    #     ('P', '.png'),
    # )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    caption = db.Column(db.String(300))
    angelpup = db.Column(db.Boolean)
    filetype = db.Column(db.Enum('.jpg', '.png'))
    # category = db.relationship('Category', backref='image', lazy='dynamic')
    hidden = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime)

    def __unicode__(self):
        return u'%s' % (self.name)

    def move_up(self):
        pass

    def move_down(self):
        pass

    class Meta:
        ordering = ['-date_added']


class ImageDemo():
    def __init__(self, id=1, name="Ashas", caption="This is a sample caption", angelpup=False):
        self.id = id
        self.name = name
        self.caption = caption
        self.filetype = '.jpg'
        self.angelpup = angelpup

    def __str__(self):
        return render_template('image.html', image=self)

    def permalink(self):
        return url_for('single', id=self.id)
