[![](https://img.shields.io/badge/officially-hacker-red?logo=verizon)](https://github.com/RITRedteam)
[![](https://img.shields.io/badge/destroys-blueteam-blue?logo=codeigniter)](https://github.com/RITRedteam)
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

## Deploying the Ark

Deployment of the Ark is done best through [docker-compose](./docs/docker.md). This allows for easy configuration and can be spun up and deployed in one command.

### Configuration
Configuration of the Ark is done in two ways
1. Environment Variables
2. Config file

Each of the methods configures a different element of the program

__Sample Configuration File__  
The config file is located by default in `config.yml` and is completely _OPTIONAL_. If no config file is specified, the default network will be used for address discovery. However, if you would like to specify certain other networks or blacklist certain addresses and hosts, the configuration file can be used.
```
# Manually specify the interface to use
interface: eth0

valid:
  - default # This will pull the network and netmask from the default gateway
  - 10.2.0.0/16 # Allow this network

invalid:
  - 10.2.1.10/24 # This network will not be in the pool
  - 10.2.255.254 # Invalidate a single IP
```

__Environment Variables__  
Several different environment variables are specified, to see usage for how to deploy with these environment variables, see the [documentation](./docs/environment.md)