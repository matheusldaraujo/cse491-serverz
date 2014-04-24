# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image, javascript, css
import os



def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    os.system("bash create_db.sh")
    html.init_templates()
    javascript.init_javascript()
    css.init_css()

    some_data = open('imageapp/dice.png', 'rb').read()
    image.add_image(some_data, "dice.png")

    some_data = open('imageapp/tux.png', 'rb').read()
    image.add_image(some_data, "tux.png")
    

def teardown():                         # stuff that should be run once.
    pass
