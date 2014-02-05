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

# Test a basic GET call.
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = '''
HTTP/1.0 200 OK
Content-Type: text/html

<a href="/content">Content</a>
<a href="/file">File</a>
<a href="/image">image</a>
<a href="/form">Form</a>
                  '''

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = '''
HTTP/1.0 200 OK
Content-Type: text/html

Content's Content
                  '''
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = '''
HTTP/1.0 200 OK
Content-Type: text/html

File's Content
                  '''
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = '''
HTTP/1.0 200 OK
Content-Type: text/html

Image's Content
                  '''
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)


def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\rn\rn")
    expected_return = "Hello World"
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)

#-----------
#Homework 3
#-----------
def test_handle_connection_get_form():
    conn = FakeConnection("GET /submit?firstname=joao&lastname=da+silva HTTP/1.0\rn\rn")
    expected_return = '''
HTTP/1.0 200 OK
Content-Type: text/html

Hello Mr. joao da silva
                  '''
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)

def test_handle_connection_post_form():
    conn = FakeConnection("POST /submit HTTP/1.0\r\nHost: w3schools.com\r\n\r\nfirstname=Joao&lastname=da Silva")
    expected_return = '''
HTTP/1.0 200 OK
Content-Type: text/html

Hello Mr. Joao da Silva
                  '''
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)