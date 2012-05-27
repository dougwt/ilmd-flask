from flask.views import MethodView
from flask import render_template, url_for, redirect
from ilovemydachshund import models


class Home(MethodView):
    def get(self):
        title = "Home"
        image = models.ImageDemo()
        images = [image, image, image, image, image]
        return render_template('home.html', title=title, images=images)


class Single(MethodView):
    def get(self, id):
        if int(id) != 1:
            return redirect(url_for('home'))
        image = models.ImageDemo()
        title = image.name
        return render_template('single.html', title=title, image=image)
