#!/usr/bin/env python
import random
import socket
import time

# This method handles the get requests
def get_request(conn, path):
    if path == '/':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Hello World!</h1>')
        conn.send("This is leflerja's Web server<br>")
        conn.send("<a href='/content'>Content</a><br>")
        conn.send("<a href='/files'>Files</a><br>")
        conn.send("<a href='/images'>Images</a>")
    elif path == '/content':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Content Page</h1>')
        conn.send('This is the content page')
    elif path == '/files':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Files Page</h1>')
        conn.send('This is the files page')
    elif path == '/images':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Images Page</h1>')
        conn.send('This is the images page')
    conn.send('</body></html>')

# This method handles the post requests
def post_request(conn):
    conn.send('HTTP/1.0 200 OK\r\n\r\n')
    conn.send('This is a post request')

# This method determines the type of request and calls the proper method
def handle_connection(conn):
    req = conn.recv(1000)
    request_type = req.split('\r\n')[0].split(' ')[0]
    if request_type == 'GET':
        path = req.split('\r\n')[0].split(' ')[1]
        get_request(conn, path)
    elif request_type == 'POST':
        post_request(conn)
    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

if __name__ == '__main__':
    main()
