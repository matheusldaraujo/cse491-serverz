#!/usr/bin/env python
# @john3209 I reviewed this, it looks great
import random
import socket
import time

def handle_post(path,conn):
    conn.send("Hello World")

def handle_get(path,conn):
    if path == "/":
        conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

<a href="/content">Content</a>
<a href="/file">File</a>
<a href="/image">image</a>
                  ''')
    if path == "/content":
        conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

Content's Content
                  ''')

    if path == "/file":
        conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

File's Content
                  ''')


    if path == "/image":
        conn.send('''
HTTP/1.0 200 OK
Content-Type: text/html

Image's Content
                  ''')

def handle_connection(conn):
    received = conn.recv(1000)
    path = received.split(" ")[1]
    mode = received.split(" ")[0]
    if mode == "POST":
        handle_post(path,conn)
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

