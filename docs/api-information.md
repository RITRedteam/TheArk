# API: Getting Information
API functions for requesting information from the server.

## /getAddresses
Get assigned addreses from The Ark for the given Halo. You may specify a count in which the server will return `count`
number of random addresses from the pool, this is useful for getting a random IP address to use from The Ark.
If no `count` is specified, The Ark will return all of the addresses for the Halo.

__Type:__ `GET`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| haloName | string   | no                 | The name of the Halo                           |
|  count   | integer  | yes (None)         | The number of IP addresses to query from The Ark |
|  unused  | bool     | yes (false)        | Ask the server to validate that the IP is unused |

__Request Example:__
```json
{
    "haloName": "ServerName",
    "count": 1,
    "unused": true
}
```

__Response Example:__
```json
{
    "haloName": "ServerName",
    "addresses": [
        "1.1.1.1"
    ]
}
```


## /addAddresses
Add the specified number of unused addresses to the registered halo name. Returns all the addresses registered
for that halo.

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| haloName | string   | no                 | The name of the Halo                           |
|  count   | integer  | yes (15)           | The number of IP addresses to query from The Ark |

__Request Example:__
```json
{
    "haloName": "ServerName",
    "count": 1,
}
```

__Response Example:__
```json
{
    "haloName": "ServerName",
    "addresses": [
        "1.1.1.1"
    ]
}
```
