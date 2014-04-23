import os
import jinja2
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from image import add_image, get_latest_image

app = Flask(__name__)

template_dir = './template'
loader = None
env = None

# Jinja
def init_templates():
    global loader, env

    # calculate the location of the templates directory relative to the
    # directory this file is in
    dirname = os.path.dirname(__file__)
    t_dir = os.path.join(dirname, template_dir)
    t_dir = os.path.abspath(t_dir)

    print 'loading templates from:', t_dir

    loader = jinja2.FileSystemLoader(t_dir)
    env = jinja2.Environment(loader=loader)

def render(template_name, values={}):
    template = env.get_template(template_name)
    return template.render(values)



# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/upload_receive", methods=['GET', 'POST'])
def upload_receive():
    the_file = request.files["file"]
    print dir(the_file)
    print 'received file with name:', the_file.filename
    data = the_file.read(int(1e9))
    add_image(data)

    return redirect("/")

@app.route("/image")
def image():
    return render_template("image.html")

@app.route("/image_raw")
def image_raw():
    img = get_latest_image()
    return img

if __name__ == "__main__":
    app.debug = True
    # Initiate with tux.png
    tux = open("tux.png")
    add_image(tux.read())
    tux.close()
    app.run()
