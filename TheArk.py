#!/usr/bin/env python3
import os
from theark import app
from theark.database import Database
from theark.hosts import Hosts

def setup():
    """Setup all the variables and run all the actions needed for The Ark to run

    1. Open a database, create it if necessary
    2. Find the original IP of the host
    """
    # Import the routes
    # Open a database
    db_name = os.environ.get("ARK_DATABASE", "files/theark.sqlite")
    config = os.environ.get("ARK_CONFIG", "config.yml")
    app.config['DATABASE'] = Database(db_name, 'files/layout.sql')
    app.config['HOSTS'] = Hosts(config, app.config['DATABASE'])
    from theark import routes, api  # pylint: disable=w0612


def cleanup():
    """Delete all the virtual interfaces for the machine
    
    TODO: Delete all the virtual interfaces for the machine
    """
    app.config['DATABASE'].close()

if __name__ == "__main__":
    setup()
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    try:
        port = os.environ.get("FLASK_PORT", "5000")
        port = int(port)
    except ValueError:
        port = 5000
    debug = os.environ.get("FLASK_DEBUG", "True")
    debug = debug.lower().strip() in ["true", "yes", "1", "t"]
    app.run(debug=debug, host=host, port=port)
    cleanup()
