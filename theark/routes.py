from flask import request, redirect, render_template, url_for, flash, make_response, jsonify

from . import app, is_authed, USERNAME, PASSWORD, COOKIE_KEY, COOKIE_VALUE

@app.route('/')
def main():
    if is_authed(request):
        return "The Ark is now running"
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to the server, Post user/pass either via form or via json
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json(force=True)
            username = data.get('username','')
            password = data.get('password','')
            if username==USERNAME and password==PASSWORD:
                return jsonify({"auth-token": COOKIE_VALUE})
            else:
                return jsonify({"error": "Incorrect username or password"})
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