#!/usr/bin/env python
# @john3209 I reviewed this, it looks great
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
import StringIO
import jinja2

# this sets up jinja2 to load templates from the 'templates' directory
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)

#Page Methods
def page_index(conn):
    template = env.get_template("index.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                      Content-Type: text/html\r\n\r\n"
    http_response += template.render(vars={})
    conn.send(http_response)

def page_file(conn):
    template = env.get_template("file.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                       Content-Type: text/html\r\n\r\n"
    http_response += template.render(vars={})
    conn.send(http_response)

def page_image(conn):
    template = env.get_template("image.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                       Content-Type: text/html\r\n\r\n"
    http_response += template.render(vars={})
    conn.send(http_response)

def page_content(conn):
    template = env.get_template("content.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                       Content-Type: text/html\r\n\r\n"
    http_response += template.render(vars={})
    conn.send(http_response)

def page_form(conn):
    template = env.get_template("form.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                       Content-Type: text/html\r\n\r\n"
    http_response += template.render(vars={})
    conn.send(http_response)

def action_submit(conn,params):
    template = env.get_template("submit.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                       Content-Type: text/html\r\n\r\n"

    vars = {"firstname":params["firstname"], "lastname":params["lastname"]}
    http_response += template.render(vars)
    conn.send(http_response)

def page_404(conn,params):
    template = env.get_template("404.html")
    http_response =   "HTTP/1.0 200 OK\r\n\
                       Content-Type: text/html\r\n\r\n"
    http_response += template.render(vars={})
    conn.send(http_response)

#HTTP Process Rquest
def handle_post(received,conn):
    #Parse the http
    headers = []
    body = ""
    get_content = False
    
    requestIO = StringIO.StringIO()
    headers_dict = {}
    
    
    #Get headers before break line than get body message
    for line in received.split("\r\n"):
        if line == "":
            get_content = True
        
        elif get_content:
            requestIO.write(line)
            continue        
        
        else:
            #Header has ':'
            if ":" in line:
                #Get header
                key = line.split(":")[0]
                val = line.split(":")[1][1:]
                headers_dict[key] = val
    
    requestIO.seek(0)
    environ = dict(REQUEST_METHOD = 'POST')
    form = cgi.FieldStorage(fp = requestIO, headers=headers_dict, environ=environ)

    #Create params like dictionary to be the same as GET
    params = {}
    for key in form.keys():
        params[key] = form[key].value

    #Get Path
    path = received.split(" ")[1]
 
    #Process for each path
    if path == "/submit":
       action_submit(conn,params)

    #Default for any path no specific
    else:
        conn.send("Hello World")
    

def handle_get(path,conn):
    #Parse the http
    parse = urlparse(path)
    path = parse.path
    params = parse_qs(parse.query)

    #Process for each path
    if path == "/":
        page_index(conn)
    elif path == "/content":
        page_content(conn)
    elif path == "/file":
        page_file(conn)
    elif path == "/image":
        page_image(conn)
    elif path == "/form":
        page_form(conn)
    elif path == "/submit":
        action_submit(conn,params)
    else:
        page_404(conn,params)
        

def handle_connection(conn):
    receivedI = StringIO.StringIO()
    #Set socket to hangs when stops to receive data    
    try:
        while True:
            receivedI.write(conn.recv(1))
            conn.setblocking(0)
    except Exception as error:
        #Check if it is the expected error, if not raise it again
        if error.args[0] == 11: #error.errno == 11 change to args[0] to work in test either
            pass
        else:
            raise(error)

    received = receivedI.getvalue()

    path = received.split(" ")[1]
    mode = received.split(" ")[0]
    if mode == "POST":
        handle_post(received,conn)
    if mode == "GET":
        handle_get(path,conn)

#    else:
#        conn.send('''
#HTTP/1.0 200 OK
#Content-Type: text/html
#
#<h1> Hello, world! </h1>
#This is araujoma's Web server </br>
#    ''')
    conn.close()



def main():
    s = socket.socket()         # Create a socket object

    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
#    port = 8080
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'

    while True:
        # Establish connection with client.

        conn, (client_ip,clienti_port) = s.accept()
        handle_connection(conn)

if __name__ == "__main__":
    main()

