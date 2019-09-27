# Set up the flask app to be imported
import os
from flask import Flask


USERNAME = os.environ.get("ARK_USERNAME", 'admin')
PASSWORD = os.environ.get("ARK_PASSWORD", 'changeme')
COOKIE_KEY = 'redteam-cookie'
COOKIE_VALUE = os.environ.get("ARK_COOKIE", 'super-secret')

app = Flask(__name__)
app.secret_key = b'magic ip addresses'

def is_authed(request):
    if COOKIE_KEY in request.cookies and request.cookies[COOKIE_KEY] == COOKIE_VALUE:
        return True
    try:
        if request.get_json(force=True).get("auth-token", "") == COOKIE_VALUE:
            return True
    except Exception as E:
        print(type(E), E)
        return False
    return False