from flask import request, redirect, render_template, url_for, flash, make_response

from . import app, is_authed, USERNAME, PASSWORD, COOKIE_KEY, COOKIE_VALUE

@app.route('/')
def main():
    if is_authed(request):
        return "The Ark is now running"
    else:
        return redirect(url_for('login'))

@app.route('/requestIps', methods=['GET', 'POST'])
def api_requestIps():
    """Handle a request for X ammount of IP addresses.
    Mark all the IPs down in the database under the server name, but DONT assign them to the interface
    Return the list of IPs for the server
    Maybe cap X so that they cant reserve all the ips
    TODO
    """
    return "not implemented"

@app.route('/requestRedirect', methods=['GET', 'POST'])
def api_requestRedirect():
    """Handle a request for an nginx redirection of X ip addresses.
    Gather X ips and assign them to virtual aliases, mark them down in the DB
    Generate an nginx server block that listens on the ips, for each of the PORTS specified
    Return the list of IPs to the client so they can use them
    Maybe cap X so that they cant reserve all the ips
    TODO
    """
    return "not implemented"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username==USERNAME and password==PASSWORD:
            resp = make_response(redirect(url_for('main')))
            resp.set_cookie(COOKIE_KEY, COOKIE_VALUE)
            return resp
        flash('Incorrect Username or Password')
        return redirect(request.url)
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie(COOKIE_KEY, COOKIE_VALUE, expires=0)
    return resp