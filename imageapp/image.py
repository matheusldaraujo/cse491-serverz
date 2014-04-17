# image handling API
from PIL import Image
from StringIO import StringIO
import base64
import sqlite3 as lite

# images = {}
# thumbs = {}
DB_path = "imageapp.db"

def create_thumbnail(data):
    #Resize same ratio
    img = Image.open(StringIO(data))
    basewidth = 200
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)

    #Trick way to get img, I did not figureout who te get image code from img variable without doing that
    img.save("tmp.png")
    f_img = open("tmp.png", "r")
    
    #Encode thumbs in base64
    thumb = base64.encodestring(f_img.read())
    return thumb

def add_image(data):

    thumb = create_thumbnail(data)
   
    try:
        con = lite.connect(DB_path)
        cur = con.cursor()
        #Get user_id
        user_id = cur.execute("select max(user_id) from images").fetchone()[0]
        if user_id == None:
            user_id = 0
        else:
            user_id += 1

        cur.execute('INSERT INTO images (image,thumb,user_id) VALUES (?, ?, ?)',[lite.Binary(data), thumb, user_id])
        con.commit()
        
    except lite.Error, e:
        print "Error:" + str(e)
    finally:
        if con:
            con.close()

    return user_id

def get_image(num):
    try:
        con = lite.connect(DB_path)
        cur = con.cursor()
        image = cur.execute('SELECT image from images where user_id=%d' % num).fetchone()
        if image:
            return image[0]
        else:
            return None
    
    except lite.Error, e:
        print "Error:" + str(e)
        # import ipdb;ipdb.set_trace()
        return None

    finally:
        if con:
            con.close()



def get_latest_image():
    try:
        con = lite.connect(DB_path)
        cur = con.cursor()
        image = cur.execute('SELECT image FROM images ORDER BY id DESC LIMIT 1;').fetchone()[0]

    except lite.Error, e:
        print "Error:" + str(e)

    finally:
        if con:
            con.close()
    
    return image

def delete_image(num):
    try:
        con = lite.connect(DB_path)
        cur = con.cursor()
        cur.execute('DELETE from images WHERE user_id=?', [num])
        con.commit()
        
    except lite.Error, e:
        print "Error:" + str(e)
    finally:
        if con:
            con.close()

    return "Done"

def has_image(num):
    try:
        con = lite.connect(DB_path)
        cur = con.cursor()
        exists = cur.execute('select 1 from images where user_id = ?', [num]).fetchone()

    except lite.Error, e:
        print "Error:" + str(e)

    finally:
        if con:
            pass
            # con.close()
    
    if exists == None:
        return False
    else:
        return True

def get_thumbs_list():
    try:
        con = lite.connect(DB_path)
        cur = con.cursor()
        thumbs_query = cur.execute("select thumb from images").fetchall()
        pass

    except lite.Error, e:
        print "Error:" + str(e)

    finally:
        if con:
            con.close()

    thumbs = []
    for item in thumbs_query:
        thumbs.append(item[0])
        
    return thumbs
