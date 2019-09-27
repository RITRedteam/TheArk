from flask import request, redirect, render_template, url_for, flash, make_response, jsonify

from . import app, is_authed, USERNAME, PASSWORD, COOKIE_KEY, COOKIE_VALUE

@app.route('/')
def main():
    if is_authed(request):
        database = app.config["DATABASE"]
        page = "The Ark is now running\n\n"
        # List all the IP addresses that are registered
        halos = database.get_halonames()

        halos_information = []
        for halo in halos:
            if not halo.get('server_name', False):
                continue
            halos_information += [{
                "haloName": halo,
                "addresses": database.get_addresses(halo['server_name'])
            }]
        return render_template("index.html", halos=halos_information)
    else:
        return redirect(url_for('login'))


@app.route('/debug')
def debug():
    if is_authed(request):
        hosts = app.config["HOSTS"]
        page = "The Ark is now running\n\nDefault Network: {}{}\nInterface: {}\n\n"
        page += "Blacklisted IP addresses ({}): \n\t{}\n\nPossible IP addresses ({}): \n\t{}\n"


        # List all the possible IP addresses
        config = hosts.load_config()
        hosts._update_net_settings(config)

        context = {
            "base_ip": hosts.base_ip,
            "netmask": hosts.netmask,
            "interface": hosts.interface,
            "blacklist": config.get("invalid", []),
            "hosts": config.get("valid", ["{}{}".format(hosts.base_ip, hosts.netmask)])
        }


        return render_template("debug.html", **context)
    else:
        return redirect(url_for('login'))

@app.route("/status")
def status():
    return "The Ark is running"

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