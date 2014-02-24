#!/usr/bin/env python
# @john3209 I reviewed this, it looks great
import cgi
import jinja2

# this sets up jinja2 to load templates from the 'templates' directory
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)


class MyApp(object):

    def __call__(self, environ, start_response):
        options = {'/'            : self.page_index,
                   '/content'     : self.page_content,
                   '/file'        : self.page_file,
                   '/image'       : self.page_image,
                   '/form'        : self.page_form,
                   '/submit'      : self.action_submit   }

        path = environ['PATH_INFO']
        page = options.get(path)
        if page is None:
            return [self.page_404(environ, start_response)]
        return [page(environ, start_response)]
    
    def __init__(self):
        self.type_html = [('Content-type', 'text/html')]
        self.type_image = [('Content-type', 'image/png')]
        self.type_text = [('Content-type', 'text/plain')]
        self.status = '200 OK'

    def get_file(self,filename):
        pfile = open(filename,"rb")
        data = pfile.read()
        pfile.close()
        return data

    #Page Methods
    def page_index(self,environ,start_response):
        start_response(self.status, self.type_html)
        template = env.get_template("index.html")
        http_response = template.render(vars={})
        return str(http_response)

    def page_file(self,environ,start_response):
        start_response(self.status, self.type_text)
        http_response = self.get_file("test_file.txt")
        return str(http_response)

    def page_image(self,environ,start_response):
        start_response(self.status, self.type_image)
        http_response = self.get_file("test_image.jpg")
        return str(http_response)

    def page_content(self,environ,start_response):
        start_response(self.status, self.type_html)
        template = env.get_template("content.html")
        http_response = template.render(vars={})
        return str(http_response)

    def page_form(self,environ,start_response):
        start_response(self.status, self.type_html)
        template = env.get_template("form.html")
        http_response = template.render(vars={})
        return str(http_response)

    def action_submit(self,environ,start_response):
        start_response(self.status, self.type_html)
        template = env.get_template("submit.html")
        form = cgi.FieldStorage(fp=environ.get('wsgi.input',''), environ=environ)
        params = {}

        #Create params like dictionary to be the same as GET
        params = {}
        for key in form.keys():
            params[key] = form[key].value

        vars = {"firstname":params["firstname"], "lastname":params["lastname"]}
        http_response = template.render(vars)
        return str(http_response)

    def page_404(self,environ,start_response):
        start_response(self.status, self.type_html)
        template = env.get_template("404.html")
        http_response = template.render(vars={})
        return str(http_response)
        
def make_app():
    return MyApp()

    # #HTTP Process Rquest
    # def handle_post(self,environ,start_response):
    #     #Parse the http
    #     headers = []
    #     body = ""
    #     get_content = False
        
    #     requestIO = StringIO.StringIO()
    #     headers_dict = {}
        
        
    #     #Get headers before break line than get body message
    #     for line in received.split("\r\n"):
    #         if line == "":
    #             get_content = True
            
    #         elif get_content:
    #             requestIO.write(line)
    #             continue        
            
    #         else:
    #             #Header has ':'
    #             if ":" in line:
    #                 #Get header
    #                 key = line.split(":")[0]
    #                 val = line.split(":")[1][1:]
    #                 headers_dict[key] = val
        
    #     requestIO.seek(0)
    #     environ = dict(REQUEST_METHOD = 'POST')
    #     form = cgi.FieldStorage(fp = requestIO, headers=headers_dict, environ=environ)

    #     #Create params like dictionary to be the same as GET
    #     params = {}
    #     for key in form.keys():
    #         params[key] = form[key].value

    #     #Get Path
    #     path = received.split(" ")[1]
     
    #     #Process for each path
    #     if path == "/submit":
    #        action_submit(conn,params)

    #     #Default for any path no specific
    #     else:
    #         conn.send("Hello World")
        

    # def handle_get(self,environ,start_response):
    #     #Parse the http
    #     parse = urlparse(path)
    #     path = parse.path
    #     params = parse_qs(parse.query)

    #     #Process for each path
    #     if path == "/":
    #         page_index(conn)
    #     elif path == "/content":
    #         page_content(conn)
    #     elif path == "/file":
    #         page_file(conn)
    #     elif path == "/image":
    #         page_image(conn)
    #     elif path == "/form":
    #         page_form(conn)
    #     elif path == "/submit":
    #         action_submit(conn,params)
    #     else:
    #         page_404(conn,params)
