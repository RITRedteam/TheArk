# API: Server Registration
API functions for server registration. There are two types of servers in The Ark, `default` and `redirect`.

__default servers__: Default servers request reservation of Ark IP addresses, however, The Ark does nothing else with these IPs.

__redirect servers__: For redirect servers, The Ark will reserve IP addresses, claim the IP addresses, and setup forwarders for the specified ports of the IP.

## /registerServer
Register a new `standard` server with The Ark, The Ark will then return a list of the IP
addresses that are assigned to it.

### Request
__Endpoint:__ `/registerServer`

__Type:__ `POST`

__Parameters:__
| Name     | Type     | Optional | Description                               |
|----------|----------|----------|-------------------------------------------|
| `name`   | string   | no       | The name of the server                    |
| `count`  | integer  | yes      | The number of IP addresses to reserve (max 30) |

__Example:__
```json
{
    "name": "ServerName",
    "count": 20,

}

```