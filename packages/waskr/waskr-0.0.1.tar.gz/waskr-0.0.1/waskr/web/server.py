from os import path

from bottle import response, request, redirect, route, run, view, send_file, TEMPLATE_PATH 
from model import WaskrStats 
from session import Authentication

# Fixes a call from a different path
CWD = path.abspath(__file__)
APP_CWD = path.dirname(CWD)
view_dir = APP_CWD+'/views'
TEMPLATE_PATH.append(view_dir)

# Create a session instance
session = Authentication()
session.first_run()

# Initialize the DB with proper values
CONF = None
db = WaskrStats(CONF)


@route('/')
@view('index')
def index():
    logged_in()
    user_email = request.COOKIES.get('user')
    return dict(user_email=user_email,
            last_received=db.last_insert(),
            apps=db.apps_nodes())


@route('/application/:name')
@route('/application/:name/:minutes')
@view('stats')
def interacting(name, minutes=120):
    logged_in()
    return dict(
            app_name=name,
            time_response=db.response_time(minutes),
            requests_second=db.request_time(minutes))


@route('/login', method='POST')
@view('login')
def login_post():
    email = request.forms.get('email')
    if session.authenticate(email):
        try:
            set_cookie(email)
            return dict()
        finally:
            redirect('/')
    else:
        redirect('/login')


@route('/login', method='GET')
@view('login')
def login_get():
    return dict()


@route('/static/:filename')
def static(filename):
    send_file(filename, root=APP_CWD+'/static')


@route('/favicon.ico')
def favicon():
    send_file('favicon.ico', root='static')


@route('/flot/:filename')
def flot(filename):
    send_file(filename, root=APP_CWD+'/static/flot/')


def logged_in():
    cookie = request.COOKIES.get('logged_in')
    if cookie == 'True':
        pass
    else:
        redirect("/login")


def set_cookie(email):
    response.set_cookie('logged_in', 'True', expires=+99500)
    response.set_cookie('user', email, expires=+99500)


def main(configuration=None):
    try:
        run(host='localhost', port=8080)
    except Exception, e:
        print "Couldn't start the waskr server:\n%s" % e


if __name__ == '__main__':
    main()

