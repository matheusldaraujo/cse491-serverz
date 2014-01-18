#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn()     # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port

    # New code for hw2
    response_type = "HTTP/1.0"
    response_line = "200 OK\r\n"
    content_type = "Content-Type: text/html\r\n\r\n"
    response_body = "<html><body> \
                     <h1>Hello, world</h1> this is leflerja's Web server \
                     </body></html>"

    c.send(response_type + ' ' + response_line)
    c.send(content_type)
    c.send(response_body)

    c.close()

