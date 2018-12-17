# Test the API by adding some data

from arkclient import ArkClient

client = ArkClient("http://192.168.177.194:5000")

def main():
    print("logging in")
    name = "test-server"
    if not client.login("admin", "password"):
        raise Exception("Couldnt log in")
    print("registering server")
    reg = client.registerServer(name)
    print("Getting addresses: ", end="")
    addrs = client.getAddresses(name)
    # Check that the responses are the same
    assert reg['addresses'] == addrs['addresses'], "Addresses are not the same length"
    assert reg['name'] == addrs['name'] == name, "server name is wrong"
    addrs = client.getAddresses(name, 1)
    assert len(addrs['addresses']) == 1
    print(addrs['addresses'][0])


if __name__ == "__main__":
    main()    