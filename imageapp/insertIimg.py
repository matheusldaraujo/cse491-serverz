import sqlite3 as lite
import base64
try:
    con = lite.connect("imageapp.db")
    cur = con.cursor()
    cur.execute('SELECT * from images')
    data = cur.fetchone()
    print data
    f_img = open("tux.png")
    img = f_img.read()
    f_img.close()
    thumb = base64.encodestring(img)
    cur.execute('INSERT INTO images (image,thumb,user_id) VALUES (?,?,1)',[lite.Binary(img), thumb])
    cur.execute('SELECT * from images')
    data = cur.fetchone()
    import ipdb;ipdb.set_trace()
    print data


except lite.Error, e:
    print "Error:" + str(e)

finally:
    if con:
        con.close()

new_img = data[1]
f_new_img = open("new_img.png","w")
f_new_img.write(new_img)
f_new_img.close()
