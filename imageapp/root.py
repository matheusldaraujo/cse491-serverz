import quixote
from quixote.directory import Directory, export, subdir
from mimetypes import guess_type
from . import html, image, javascript, css
import json

class RootDirectory(Directory):
    _q_exports = ["_q_lookup","teste","_q_index"]

    def check_has_image(self):
        request = quixote.get_request()
        toGet = request.get_cookie("img_id")
        if toGet == None or toGet == "":
            return False
        else:
            return image.has_image(int(toGet))

    def get_image_raw(self,path):
        if len(path) == 2 and "image_raw" in path[0]:
            image_request = int(path[1])
            image_db = image.get_image(image_request)
            if image_db[0]:
                response = quixote.get_response()
                response.set_content_type(guess_type(image_db[1])[0])
                return image_db[0]
            else:
                return "Invalid Image ID"
        return None

    def _q_traverse(self,path):
        try:
            #Project 23
            #Handle raw_image get by ID, example http://localhost/image_raw/1
            image_raw = self.get_image_raw(path)
            if image_raw:
                return image_raw
            
            if path[0] == "":
                return self.index()

            if path[0] == "upload":
                return self.upload()

            if path[0] == "upload_receive":
                return self.upload_receive()

            if path[0] == "image":
                return self.image()

            if path[0] == "upload":
                return self.upload()

            if path[0] == "get_image":
                return self.get_image()

            if path[0] == "delete":
                return self.delete()

            if path[0] == "jquery.js":
                return self.jquery()

            if path[0] == "ajax_upload_image.js":
                return self.ajax_upload()

            if path[0] == "style.css":
                return self.style_css_upload()

            if path[0] == "list_thumbs":
                return self.thumbs()

        except Exception, e:
            # Not an integer
            print "Error:" + str(e)
        
        return "404"

    def index(self):
        return html.render('index.html', {"has_image":self.check_has_image()})

    
    def upload(self):
        request = quixote.get_request()
        img_id = None
        
        if request.cookies.has_key("img_id"):
            img_id = request.cookies["img_id"]
        
        return html.render('upload.html', {"has_image":self.check_has_image(), "img_id":img_id})
        
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        img_id = image.add_image(data,the_file.base_filename)

        return str(img_id)

    def image(self):
        return html.render('image.html', {"has_image":self.check_has_image()})

    def delete(self):
        request = quixote.get_request()
        toDelete = request.form['img_id']
        image.delete_image(int(toDelete))
        return "Done"

    def jquery(self):
        return javascript.render("jquery-1.11.0.min.js")

    def ajax_upload(self):
        return javascript.render("ajax_upload_image.js")

    def style_css_upload(self):
        return css.render("style.css")

    def thumbs(self):
        return html.render('thumbs.html', {"thumbs":image.get_thumbs_list()})

    def get_image(self):
        response = quixote.get_response()
        request = quixote.get_request()
        toGet = request.get_cookie("img_id")
        if image.has_image(int(toGet)):
            img_db = image.get_image(int(toGet))
            response.set_content_type(guess_type(img_db[1])[0])
            return img_db[0]
        return "You have no image!"
