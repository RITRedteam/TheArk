# The Ark
The Ark manages virtual IP addresses for redteam tools. It is responsible for being the single source of truth for which virtual IPs are assigned to what redteam tools. Tools can request a list of virtual IP addressses to have reserved (e.g. [Sangheili](https://github.com/RITRedteam/Sangheili)), and the Ark will search through the network for unused IP addresses. Because the mappings need to be persistent, The Ark writes the mappings to a Sqlite3 database.

## Documentation
Im trying hard to document the code and document the API and usage and such. You can read all the documentation [here](./docs/)

## The Ark Server
The Ark server provides API endpoints for tools to reserve IP addresses.

## Halos
Each server that is registered with the Ark is called a `halo`. Each Halo is assigned a group of IP addresses for its own use. 

> The Ark does nothing with these addresses, it simply marks them as reserved. If you would like to
redirect traffic using these addresses, see [Halo](https://github.com/RITRedteam/TheArkHalo).

## API Documentation
Currently the API documentation describes all the different functions that The Ark implements.
You can read the API documentation [here](./docs/api.md).


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

## Contributing
If you want to work on this, just follow the TODOs for now