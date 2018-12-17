#!/usr/bin/env python3
from theark import app
from theark.database import Database
from theark.networking import net_init

def setup():
    """Setup all the variables and run all the actions needed for The Ark to run

    1. Open a database, create it if necessary
    2. Find the original IP of the host
    """
    # Open a database
    app.config['DATABASE'] = Database('files/theark.sqlite', 'files/layout.sql')
    app.config['networking'] = {}
    net_init()

def cleanup():
    """Delete all the virtual interfaces for the machine
    TODO
    """
    app.config['DATABASE'].close()
    pass

if __name__ == "__main__":
    setup()
    app.run(host=app.config['networking'].get('base_ip', "0.0.0.0"), port=8080)
    cleanup()
