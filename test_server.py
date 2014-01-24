import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call for the root.
def test_handle_connection_root():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Hello World!</h1>' + \
                      'This is leflerja\'s Web server<br>' + \
                      '<a href=\'/content\'>Content</a><br>' + \
                      '<a href=\'/files\'>Files</a><br>' + \
                      '<a href=\'/images\'>Images</a>' + \
                      '</body></html>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for the root.
def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Content Page</h1>' + \
                      'This is the content page' + \
                      '</body></html>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for file.
def test_handle_connection_file():
    conn = FakeConnection("GET /files HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Files Page</h1>' + \
                      'This is the files page' + \
                      '</body></html>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for image.
def test_handle_connection_image():
    conn = FakeConnection("GET /images HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Images Page</h1>' + \
                      'This is the images page' + \
                      '</body></html>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a POST call.
def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n\r\n' + \
                      'This is a post request'
