# Test the API by adding some data

import os
from arkclient import ArkClient

client = ArkClient(os.environ.get("THEARK_SERVER", "http://0.0.0.0:5000"))

def main():
    print("logging in")
    name = "test-server"
    if not client.login("admin", "password"):
        raise Exception("Couldnt log in")
    print("registering a new halo")
    reg = client.registerHalo(name)
    print("Getting addresses: ", end="")
    addrs = client.getAddresses(name)
    # Check that the responses are the same
    assert reg['haloName'] == addrs['haloName'] == name, "haloName is wrong"
    addrs = client.getAddresses(name, 1, True)
    assert len(addrs['addresses']) == 1
    print("Got a random IP from the server:", addrs['addresses'][0])


if __name__ == "__main__":
    main()    