This package provides a service based on JSONRPC with some small additions to the standard in order to enable authenticated requests.  The WSGI specification is used for data communication.  The package is broken down into two halves - a client and a server.  For security, the server is best run over HTTPS, although this is not enforced.

The server depends on WebOb 1.0.0 and above.  This is automatically installed if you have an internet connection, otherwise download and install from http://pypi.python.org/pypi/WebOb

If you install under Python 3, only the client package is available at the moment, until WebOb has been ported to python 3.

Example Usage (Server):

::

    import hashlib
    from wsgiref import simple_server
    from AuthRPC.server import AuthRPCApp

    def myauth(username, password, useragent):
        return username  == 'myuser' and \
               password  == hashlib.md5('secret').hexdigest() and \
               useragent == 'myprogram'

    class api(object):
        def do_something(self, myvar):
            """Your code placed here"""
            return 'Something', myvar

    application = AuthRPCApp(api(), auth=myauth)
    simple_server.make_server('localhost', 1234, application)

Example Usage (Client):

::

    from AuthRPC.client import ServerProxy
    client = ServerProxy('http://localhost:1234/',
                         username='myuser',
                         password='secret',
                         user_agent='myprogram')
    retval = client.do_something('test')

