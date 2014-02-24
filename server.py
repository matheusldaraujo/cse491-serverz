#!/usr/bin/env python
# @john3209 I reviewed this, it looks great
import random
import socket
import StringIO
from app import make_app
from urlparse import urlparse
from wsgiref.validate import validator
import sys


def handle_connection(conn,host,port):
    receivedI = StringIO.StringIO()
    # Set socket to hangs when stops to receive data
    try:
        while True:
            receivedI.write(conn.recv(1))
            conn.setblocking(0)
    except Exception as error:
        #Check if it is the expected error, if not raise it again
        #error.errno == 11 change to args[0] to work in test either
        if error.args[0] == 11:
            pass
        else:
            raise(error)

    received = receivedI.getvalue()

    headersHTTP = map(lambda x: x.split(" "), received.split("\r\n"))
    headerDic = {}
    for header in headersHTTP:
        if header[0] != "" and len(header) >= 2: #Dont get body from post
            headerDic[header[0].upper().replace(":", "").replace("-", "_")] = header[1]
    
    url = headersHTTP[0][1]
    path = urlparse(url)[2]
    query = urlparse(url)[4]
    mode = headersHTTP[0][0]

    environ = {}
    
    if mode == "POST":
        #Get POST body

        beginBody = received.find("\r\n\r\n") + len ("\r\n\r\n")
        endBody = beginBody + int(headerDic['CONTENT_LENGTH'])
        body = received[beginBody : endBody]
        
        environ['REQUEST_METHOD'] = mode
        environ['PATH_INFO'] = path
        environ['QUERY_STRING'] = query
        environ['CONTENT_TYPE'] = headerDic['CONTENT_TYPE']
        environ['CONTENT_LENGTH'] = headerDic['CONTENT_LENGTH']
        environ['SCRIPT_NAME'] = ''
        environ['SERVER_NAME'] = host
        environ['SERVER_PORT'] = str(port)
        environ['wsgi.input'] = StringIO.StringIO(body)
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.multithread'] = True
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True
        environ['wsgi.url_scheme'] = "http"
        

    if mode == "GET":
        environ['REQUEST_METHOD'] = mode
        environ['PATH_INFO'] = path
        environ['QUERY_STRING'] = query
        environ['CONTENT_TYPE'] = ''
        environ['SCRIPT_NAME'] = ''
        environ['CONTENT_LENGTH'] = str(0)
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = str(port)
        environ['wsgi.input'] = StringIO.StringIO("")
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.multithread'] = True
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True
        environ['wsgi.url_scheme'] = "http"

    #new_app = validator(make_app())
    new_app = make_app()

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    result = new_app(environ, start_response)
    for data in result:
        conn.send(data)

    conn.close()


def main():
    s = socket.socket()         # Create a socket object

    host = socket.getfqdn()  # Get local machine name
    port = random.randint(8000, 9999)
#    port = 8080
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'

    while True:
        # Establish connection with client.

        conn, (client_ip, clienti_port) = s.accept()
        handle_connection(conn,host,port)

if __name__ == "__main__":
    main()
