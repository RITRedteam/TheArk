# Test the API by adding some data

from arkclient import ArkClient

client = ArkClient("http://localhost:5000")

def main():
    print("logging in")
    if not client.login("admin", "password"):
        raise Exception("Couldnt log in")
    print("registering server")
    print(client.registerServer("test-server"))

if __name__ == "__main__":
    main()    