import quixote
from quixote.directory import Directory, export, subdir

from . import html, image, javascript, css
import json

class RootDirectory(Directory):
    _q_exports = []

    def check_has_image(elf):
        request = quixote.get_request()
        toGet = request.get_cookie("img_id")
        if toGet == None or toGet == "":
            return False
        else:
            return image.has_image(int(toGet))

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html', {"has_image":self.check_has_image()})

    
    @export(name='upload')
    def upload(self):
        return html.render('upload.html', {"has_image":self.check_has_image()})
        

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        img_id = image.add_image(data)

        return str(img_id)

    @export(name='image')
    def image(self):
        return html.render('image.html', {"has_image":self.check_has_image()})

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('image/png')
        img = image.get_latest_image()
        return img

    @export(name='get_image')
    def get_image(self):
        response = quixote.get_response()
        response.set_content_type('image/png')
        request = quixote.get_request()
        toGet = request.get_cookie("img_id")
        if image.has_image(int(toGet)):
            img = image.get_image(int(toGet))
            return img
        return "You have no image!"

    

    @export(name='delete')
    def delete(self):
        request = quixote.get_request()
        toDelete = request.form['img_id']
        image.delete_image(int(toDelete))
        return "Done"


    @export(name='jquery.js')
    def jquery(self):
        return javascript.render("jquery-1.11.0.min.js")

    @export(name='ajax_upload_image.js')
    def ajax_upload(self):
        return javascript.render("ajax_upload_image.js")

    @export(name='style.css')
    def style_css_upload(self):
        return css.render("style.css")
