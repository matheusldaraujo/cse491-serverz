# image handling API
from PIL import Image
from StringIO import StringIO
import base64

images = {}
thumbs = {}


def add_image(data):
    img = Image.open(StringIO(data))

    if images:
        image_num = max(images.keys()) + 1

    else:
        image_num = 0
        
    images[image_num] = data
    
    #Resize same ratio
    basewidth = 200
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    
    img.save("tmp.png")
    f_img = open("tmp.png", "r")
    
    thumbs[image_num] = base64.encodestring(f_img.read())

    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

def delete_image(num):
    images.pop(num)
    return "Done"

def has_image(num):
    return images.has_key(num)

def get_thumbs_list():
    return thumbs
