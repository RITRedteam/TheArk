import random
from flask import request, abort, jsonify

from . import app, is_authed
#from .networking import discover_hosts, is_ip_taken



database = app.config["DATABASE"]
hosts = app.config["HOSTS"]

@app.route('/registerHalo', methods=['POST'])
def registerHalo():
    """Register a new Halo with TheArk
    
    See docs/api-halos.md for json spec
    """
    if not is_authed(request): abort(403)
    data = request.get_json(force=True)
    # Validate required params
    if 'haloName' not in data:
        return jsonify({"error": "'haloName' must be specified"}), 400
    name = data['haloName']
    if database.is_haloname_taken(name):
        return jsonify({"error": "'{}' is already taken as a Halo name".format(name)}), 400
    count = 15
    if 'count' in data and data['count'] != None:
        try:
            count = int(data['count'])
        except ValueError:
            return jsonify({"error": "'count' must be an integer > 0"}), 400
    _type = 'default'
    addresses = hosts.discover_hosts(count)
    database.add_halo(_type, data)
    database.add_addresses(name, addresses)
    database.commit()
    return jsonify({
        "haloName": name,
        "addresses": addresses
    })


@app.route('/addAddresses', methods=['POST'])
def addAddresses():
    """Adds a new set of IP address to a halo
    
    See docs/api-information.md for json spec
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    # Validate required params
    if 'haloName' not in data:
        return jsonify({"error": "'haloName' must be specified"}), 400
    name = data['haloName']
    if not database.is_haloname_taken(name):
        return jsonify({"error": "'{}' is not a registered Halo name".format(name)}), 400
    count = 15 # Default to 15 new IPs
    if 'count' in data and data['count'] != None:
        try:
            count = int(data['count'])
        except ValueError:
            return jsonify({"error": "'count' must be an integer > 0"}), 400
    
    addresses = hosts.discover_hosts(count)
    database.add_addresses(name, addresses)
    database.commit()
    addresses = database.get_addresses(name)
    return jsonify({
        "haloName": name,
        "addresses": addresses
    })


@app.route('/deleteHalo', methods=['POST'])
def deleteHalo():
    """Delete a halo from TheArk
    
    See docs/api-halos.md for json spec
    
    TODO: Implement this function
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    data['error'] = "API call not yet implemented"
    return jsonify(data)


@app.route('/getAddresses', methods=['GET'])
def getAddresses():
    """Get ip addresses associated with the halo name
    
    See docs/api-information.md for json spec
    """
    if not is_authed(request):  abort(403)
    data = request.get_json(force=True)
    # Validate required params
    if 'haloName' not in data:
        return jsonify({"error": "'haloName' must be specified"}), 400
    name = data['haloName']
    if not database.is_haloname_taken(name):
        return jsonify({"error": "'{}' is not a registered Halo name".format(name)}), 400
    count = None
    if 'count' in data and data['count'] != None:
        try:
            count = int(data['count'])
        except ValueError:
            return jsonify({"error": "'count' must be an integer > 0"}), 400
    
    addrs = database.get_addresses(data['haloName'])  # Get all the addresses for name from db

    retval = {}
    retval['haloName'] = data['haloName']

    # If req is only for X num of ips, shuffle it and return random X count
    if count and count < len(addrs):
        random.shuffle(addrs)
        retval['addresses'] = []
        for _ in range(count):
            # Make sure we have ips to pull from
            if not addrs:
                break
            addr = addrs.pop()  # Get a random IP
            # If we are asked to only return unused ip addresses
            if data.get('unused', False):
                if hosts.is_ip_taken(addr):
                    continue  # If the ip is in use, move to the next one
            retval['addresses'] += [addr]
    else:
        # Else just return all the addrs
        retval['addresses'] = addrs

    return jsonify(retval)


@app.route('/getHalos', methods=['GET'])
def getHalos():
    """Return all the registered halos from the The Ark
    """
    if not is_authed(request):  abort(403)
    halos = database.get_halonames()
    halos = [server['server_name'] for server in halos if server.get('server_name', False)]
    data = {
        'halos': halos
    }
    return jsonify(data)
