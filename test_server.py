import server

host = "localhost"
port = "8080"


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
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = ["200","Content page"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = ["200","THE FIRST BOOK OF MOSES, CALLED GENESIS"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = ["200","Content-type: image/png"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = ["200","input","submit","firstname"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_post():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: "+ str(len("firstname=Joao&lastname=da Silva")) + "\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                          "firstname=Joao&lastname=da Silva")
    server.handle_connection(conn,host,port)
    assert 'HTTP/1.0 200 OK' in conn.sent, "Got: %s" % (repr(conn.sent),)

#-----------
#Homework 3
#-----------

def test_handle_connection_get_submit():
    conn = FakeConnection("GET /submit?firstname=joao&lastname=da+silva HTTP/1.0\rn\rn")
    expected_return = ["200","joao","silva"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post_submit():
    conn = FakeConnection("POST /submit HTTP/1.0\r\nHost: w3schools.com\r\nConnection: keep-alive\r\nContent-Length: " + str(len("firstname=Joao&lastname=da Silva")) + "\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nOrigin: http://bota:8918\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36\r\nContent-Type: application/x-www-form-urlencoded\r\nReferer: http://bota:8918/form\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en-US,en;q=0.8,pt;q=0.6\r\n\r\nfirstname=Luis&lastname=da Silva")
    expected_return = ["200","Luis","Silva"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

#-----------
#Homework 4
#-----------
def test_handle_connection_404():
    conn = FakeConnection("GET /sadasdadad HTTP/1.0\r\n\r\n")
    expected_return = ["200","404"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)

    conn = FakeConnection("GET /xzcasdq HTTP/1.0\r\n\r\n")
    expected_return = ["200","404"]
    server.handle_connection(conn,host,port)

    assert conn.check_words_in_response(expected_return), 'Got: %s' % (repr(conn.sent),)