from flask import render_template, url_for, redirect
from app import models, View
from PIL import Image as PILimage


class Home(View):
    def get(self):
        title = "Home"
        images = models.Image.query.all()
        return render_template('home.html', title=title, images=images)


class Single(View):
    def get(self, id):
        image = models.Image.query.get(int(id))
        if not image:
            return redirect(url_for('home'))
        title = image.name
        return render_template('single.html', title=title, image=image)


def generate_thumbnail(image, path='app/static/gallery/', width=128, height=128):
    original_filepath = path + str(image.id) + image.filetype
    new_filepath = path + str(image.id) + '.thumb' + image.filetype
    img = PILimage.open(original_filepath)
    box = width, height
    out = open(new_filepath, 'w')
    resize_image(img, box, True, out)


def generate_largest(image, path='app/static/gallery/', width=800, height=600):
    original_filepath = path + str(image.id) + image.filetype
    new_filepath = path + str(image.id) + '.large' + image.filetype
    img = PILimage.open(original_filepath)
    box = width, height
    out = open(new_filepath, 'w')
    resize_image(img, box, False, out)


def resize_image(img, box, fit, out):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
    @param out: file-like-object - save the image into the output stream
    '''
    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
        factor *= 2
    if factor > 1:
        img.thumbnail((img.size[0] / factor, img.size[1] / factor), PILimage.NEAREST)

    #calculate the cropping box and get the cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / box[0]
        hRatio = 1.0 * y2 / box[1]
        if hRatio > wRatio:
            y1 = int(y2 / 2 - box[1] * wRatio / 2)
            y2 = int(y2 / 2 + box[1] * wRatio / 2)
        else:
            x1 = int(x2 / 2 - box[0] * hRatio / 2)
            x2 = int(x2 / 2 + box[0] * hRatio / 2)
        img = img.crop((x1, y1, x2, y2))

    #Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, PILimage.ANTIALIAS)

    #save it into a file-like object
    img.save(out, "JPEG", quality=75)
