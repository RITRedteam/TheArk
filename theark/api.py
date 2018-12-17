import random
from flask import request, abort, jsonify

from . import app, is_authed
from .networking import discover_hosts



database = app.config["DATABASE"]

@app.route('/registerServer', methods=['POST'])
def registerServer():
    """Register a new server with TheArk
    
    See docs/api-servers.md for json spec
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    # Validate required params
    if 'name' not in data:
        return jsonify({"error": "'name' must be specified"})
    name = data['name']
    if database.is_servername_taken(name):
        return jsonify({"error": "'{}' is already taken as a server name".format(name)})
    count = 15
    if 'count' in data and data['count'] != None:
        try:
            count = int(data['count'])
        except ValueError:
            return jsonify({"error": "'count' must be an integer > 0"})
    _type = 'default'
    addresses = discover_hosts(count)
    database.add_server(_type, data)
    database.add_addresses(name, addresses)
    database.commit()
    return jsonify({
        "name": name,
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
    """Get ip addresses associated with the server name
    
    See docs/api-information.md for json spec
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    # Validate required params
    if 'name' not in data:
        return jsonify({"error": "'name' must be specified"})
    count = None
    if 'count' in data and data['count'] != None:
        try:
            count = int(data['count'])
        except ValueError:
            return jsonify({"error": "'count' must be an integer > 0"})
    
    addrs = database.get_addresses(data['name'])  # Get all the addresses for name from db

    retval = {}
    retval['name'] = data['name']

    # If req is only for X num of ips, shuffle it and return random X count
    if count and count < len(addrs):
        random.shuffle(addrs)
        retval['addresses'] = [addrs.pop() for i in range(count)]
    else:
        # Else just return all the addrs
        retval['addresses'] = addrs

    return jsonify(retval)


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
