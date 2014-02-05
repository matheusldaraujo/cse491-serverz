#!/usr/bin/env python
# @john3209 I reviewed this, it looks great
import random
import socket
import time
from urlparse import urlparse, parse_qs

#Page Methods
def page_index(conn):
    conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

<a href="/content">Content</a>
<a href="/file">File</a>
<a href="/image">image</a>
<a href="/form">Form</a>
                  ''')
def page_file(conn):
    conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

File's Content
                  ''')
def page_image(conn):
    conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

Image's Content
                  ''')
def page_content(conn):
    conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

Content's Content
                  ''')
def page_form(conn):
    conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

<form action='/submit' method='POST'>
<input type='text' name='firstname'>
<input type='text' name='lastname'>
<input type="submit" value="Submit">
</form>
                  ''')

def action_submit(conn,params):
    conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

Hello Mr. %s %s
                  ''' % (params["firstname"][0], params["lastname"][0]))

#HTTP Process Rquest
def handle_post(received,conn):
    #Parse the http
    headers = []
    body = ""
    get_body = False
   
    for line in received.split("\r\n"):
        if get_body:
            body = line
            continue
        if line == "":
            get_body = True
        headers.append(line)
    
    path = received.split(" ")[1]
    params = parse_qs(body)
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
    if path == "/content":
        page_content(conn)
    if path == "/file":
        page_file(conn)
    if path == "/image":
        page_image(conn)
    if path == "/form":
        page_form(conn)
    if path == "/submit":
        action_submit(conn,params)
        

def handle_connection(conn):
    received = conn.recv(1000)
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

