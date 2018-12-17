# Set up the flask app to be imported

from flask import Flask

USERNAME = 'admin'
PASSWORD = 'password'
COOKIE_KEY = 'redteam-cookie'
COOKIE_VALUE = 'super-secret'

app = Flask(__name__)
app.secret_key = b'magic ip addresses'

def is_authed(request):
    if COOKIE_KEY in request.cookies and request.cookies[COOKIE_KEY] == COOKIE_VALUE:
        return True
    if request.get_json(force=True).get("auth-token", "") == COOKIE_VALUE:
        return True
    return False