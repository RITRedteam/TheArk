from flask import request, abort, jsonify
from . import app, is_authed
from .networking import discover_hosts

database = app.config["DATABASE"]

@app.route('/registerServer', methods=['POST'])
def registerServer():
    """Register a new server with TheArk
    
    See docs/api-servers.md for json spec
    TODO: Add validate of properties here
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    _type = 'default'
    addresses = discover_hosts(data.get("count", 15))
    database.add_server(_type, data)
    database.add_addresses(data.get('name'), addresses)
    return jsonify({
        "name": data.get('name'),
        "addresses": addresses
    })


@app.route('/registerRedirectServer', methods=['POST'])
def registerRedirectServer():
    """Register a new redirect server with TheArk
    
    See docs/api-servers.md for json spec
    
    TODO: Implement this function
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    data['error'] = "API call not yet implemented"
    return jsonify(data)


@app.route('/deleteServer', methods=['POST'])
def deleteServer():
    """Delete a server from TheArk
    
    See docs/api-servers.md for json spec
    
    TODO: Implement this function
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    data['error'] = "API call not yet implemented"
    return jsonify(data)


@app.route('/getAddresses', methods=['GET'])
def getAddresses():
    """Register a new redirect server with TheArk
    
    See docs/api-information.md for json spec
    
    TODO: Implement this function
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    data['error'] = "API call not yet implemented"
    return jsonify(data)


@app.route('/getServerSettings', methods=['GET'])
def getServerSettings():
    """Return the settings that are registered for the server.

    See docs/api-information.md for json spec
    
    TODO: Implement this function
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    data['error'] = "API call not yet implemented"
    return jsonify(data)


@app.route('/getNginxConfig', methods=['GET'])
def getNginxConfig():
    """If the server is a `redirect` server, return the NGINX server block
    that The Ark uses (or would use) to redirect the traffic.
    
    See docs/api-information.md for json spec
    
    TODO: Implement this function
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    data['error'] = "API call not yet implemented"
    return jsonify(data)
