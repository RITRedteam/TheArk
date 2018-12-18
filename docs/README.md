# The Ark Documentation
The Ark manages virtual IP addresses for redteam tools. It can spin up NGINX server blocks to listen on for upstreaming to redteam servers and C2s. The Ark is also responsible for being the single source of truth for which virtual IPs are assigned to what redteam tools. Tools can request a list of virtual IP addressses to have reserved (for example, [Sangheili](https://github.com/RITRedteam/Sangheili) can request a list of IPs to use for outgoing connections). Because the mappings need to be persistent, The Ark writes the mappings to a Sqlite3 database.


## API Documentation
Currently the API documentation describes all the different functions that The Ark implements.
You can read the API documentation [here](./api.md).


## Client Library
A simple client library has been implemented in `files/arkclient.py`. To start using the client library, you can run the following snippet

```python
from arkclient import ArkClient

client = ArkClient("http://localhost:5000")

if not client.login("admin", "password"):
    raise Exception("Couldnt log in")
# From here on, we are logged in. We cann now call other API functions
resp = client.registerServer("test-server")
print(resp)
```