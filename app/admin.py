from flask import render_template, url_for, redirect
from app import models, View
from flask.ext.wtf import Form, TextField, SelectField, BooleanField, Required


class SubmitImageForm(Form):
    description = TextField('description', validators=[Required()])
    category_id = SelectField('category')
    hidden = BooleanField('hidden', default=False)

    # description = db.Column(db.String(300))
    # filetype = db.Column(db.Enum('.jpg', '.png'))
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # hidden = db.Column(db.Boolean, default=True)
    # date_added = db.Column(db.DateTime)
    # likes = db.relationship('Like', backref='image', lazy='dynamic')
    # tags = db.relationship('Tag', backref='image', lazy='dynamic')


class SubmitImage(View):
    def get(self):
        title = "Title"
        form = SubmitImageForm()
        form.category_id.choices = [(g.id, g.name) for g in models.Category.query.order_by('name')]
        return render_template('form_submit_image.html', title=title, form=form, current_user=self.current_user())
