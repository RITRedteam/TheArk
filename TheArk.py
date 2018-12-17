#!/usr/bin/env python3
from theark import app
from theark.database import Database
from theark.ips import getIp, getInterfaceNameFromIp

def setup():
    """Setup all the variables and run all the actions needed for The Ark to run

    1. Open a database, create it if necessary
    2. Find the original IP of the host
    """
    # Open a database
    app.config['DATABASE'] = Database('files/theark.sqlite', 'files/layout.sql')
    app.config['networking'] = {}
    app.config['networking']['default_ip'] = getIp()
    app.config['networking']['interface'] = getInterfaceNameFromIp(app.config['networking']['default_ip'])

def cleanup():
    """Delete all the virtual interfaces for the machine
    TODO
    """
    pass

if __name__ == "__main__":
    setup()
    # TODO: Make sure we are only listening here on the original interface
    app.run(host=app.config['networking']['default_ip'], port=8080)
    cleanup()
