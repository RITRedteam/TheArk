from . import app, is_authed
from flask import request, redirect, render_template, url_for, flash, make_response

@app.route('/registerServer', methods=['POST'])
def registerServer():
    """Register a new server with TheArk
    
    See docs/api-servers.md for json spec
    """
    pass


@app.route('/registerRedirectServer', methods=['POST'])
def registerRedirectServer():
    """Register a new redirect server with TheArk
    
    See docs/api-servers.md for json spec
    """
    pass


@app.route('/deleteServer', methods=['POST'])
def deleteServer():
    """Delete a server from TheArk
    
    See docs/api-servers.md for json spec
    """
    pass

@app.route('/getAddresses', methods=['GET'])
def getAddresses():
    """Register a new redirect server with TheArk
    
    See docs/api-servers.md for json spec
    """
    pass
