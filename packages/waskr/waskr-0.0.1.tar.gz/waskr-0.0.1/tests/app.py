import sys
if '../' not in sys.path:
    sys.path.append('../')
from waskr.middleware import RequestStatsMiddleware

def application(environ, start_response):
    start_response('200 OK', [
        ('Content-Type', 'text/html')
    ])
    return ['Hello World']

if __name__ == '__main__':
    app = RequestStatsMiddleware(application)
    from wsgiref.simple_server import make_server
    httpd = make_server('', 1234, app)
    httpd.serve_forever()
