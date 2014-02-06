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

    def setblocking(self,n):
        if self.to_recv == "":
            raise Exception(11,"FakeConnection setblocking","erro")

    def check_words_in_response(self,list_words):
        response = self.sent
        for word in list_words:
            if not word in response:
                return False
        return True

# Test a basic GET call.
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = ["200","href","Content","File","Form"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = ["200","Content page"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = ["200","File's Content"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = ["200","Image's Content"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = ["200","input","submit","firstname"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\rn\rn")
    expected_return = "Hello World"
    server.handle_connection(conn)
    assert conn.sent == expected_return, "Got: %s" % (repr(conn.sent),)

#-----------
#Homework 3
#-----------

def test_handle_connection_get_submit():
    conn = FakeConnection("GET /submit?firstname=joao&lastname=da+silva HTTP/1.0\rn\rn")
    expected_return = ["200","joao","silva"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post_submit():
    conn = FakeConnection("POST /submit HTTP/1.0\r\nHost: w3schools.com\r\n\r\nfirstname=Joao&lastname=da Silva")
    expected_return = ["200","Joao","Silva"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

#-----------
#Homework 4
#-----------
def test_handle_connection_404():
    conn = FakeConnection("GET /sadasdadad HTTP/1.0\r\n\r\n")
    expected_return = ["200","404"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

    conn = FakeConnection("GET /xzcasdq HTTP/1.0\r\n\r\n")
    expected_return = ["200","404"]
    server.handle_connection(conn)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)