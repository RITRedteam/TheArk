#!/usr/bin/env python3
import os
from theark import app
from theark.database import Database
from theark.networking import net_init

def setup():
    """Setup all the variables and run all the actions needed for The Ark to run

    1. Open a database, create it if necessary
    2. Find the original IP of the host
    """
    # Import the routes
    # Open a database
    app.config['DATABASE'] = Database('files/theark.sqlite', 'files/layout.sql')
    app.config['networking'] = {}
    net_init()
    from theark import routes, api  # pylint: disable=w0612


def cleanup():
    """Delete all the virtual interfaces for the machine
    
    TODO: Delete all the virtual interfaces for the machine
    """
    app.config['DATABASE'].close()
    pass

if __name__ == "__main__":
    setup()
    host = os.environ.get("ARK_LISTEN_IP", "0.0.0.0")
    port = os.environ.get("ARK_LISTEN_PORT", "5000")

    app.run(host=host, port=port, debug=True)
    cleanup()
