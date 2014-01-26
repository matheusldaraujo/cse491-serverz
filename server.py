import random
import socket
import time
from urlparse import urlparse, parse_qs
import urllib

def request_index(conn, path):
    return '<h1>Hello World!</h1>\r\n' + \
           "This is leflerja's Web server<br>\r\n" + \
           "<a href='/content'>Content</a><br>\r\n" + \
           "<a href='/files'>Files</a><br>\r\n" + \
           "<a href='/images'>Images</a><br>\r\n" + \
           "<a href='/form'>Form</a>\r\n"

def request_content(conn, path):
    return '<h1>Content Page</h1>\r\n' + \
           'This is the content page\r\n'

def request_files(conn, path):
    return '<h1>Files Page</h1>\r\n' + \
           'This is the files page\r\n'

def request_images(conn, path):
    return '<h1>Images Page</h1>\r\n' + \
           'This is the images page\r\n'

def request_form(conn, path):
    return '<h1>Form Page</h1>\r\n' + \
           '<form action=\'/submit\' method=\'GET\'>\r\n' + \
           'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' + \
           'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' + \
           '<input type=\'submit\' name=\'submit\'>\r\n' + \
           '</form>\r\n'

def request_submit(conn, path):
    return '<h1>Submit Page</h1>\r\n' + \
           'Hello {0} {1}'.format(path['firstname'][0], path['lastname'][0])

def get_request(conn, path):
    form_keys = parse_qs(urlparse(path)[4])
    page = urlparse(path)[2]

    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<html><body>\r\n'
    footer = '</body></html>\r\n'

    # Not sure why I keep getting /favicon.ico...
    options = {'/'            : request_index,   \
               '/favicon.ico' : request_index,   \
               '/content'     : request_content, \
               '/files'       : request_files,   \
               '/images'      : request_images,  \
               '/form'        : request_form,    \
               '/submit'      : request_submit   }

    conn.send(header)
    conn.send(options[page](conn, form_keys))
    conn.send(footer)

def post_request(conn):
    conn.send('HTTP/1.0 200 OK\r\n\r\n')
    conn.send('This is a post request')

def handle_connection(conn):
    request = conn.recv(1000)
    request_type = request.split()[0]
    if request_type == 'GET':
        path = request.split()[1]
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
