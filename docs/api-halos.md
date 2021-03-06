# API: Halos
API functions for screating and deleting Halos. There are two types of Halos in The Ark, `default` and `redirect`.

__default halos__: Default Halos request reservation of Ark IP addresses, however, The Ark does nothing else with these IPs.

__redirect halos__: For redirect Halos, The Ark will reserve IP addresses, claim the IP addresses, and setup forwarders for the specified ports of the IP.

## /registerHalo
Register a new `default` Halo with The Ark, The Ark will then return a list of the IP
addresses that are assigned to it.

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| haloName | string   | no                 | The name of the Halo                           |
| count  | integer  | yes (15)           | The number of IP addresses to reserve (max 50) |

__Request Example:__
```json
{
    "haloName": "HaloName",
    "count": 20
}
```

__Response Example:__
```json
{
    "haloName": "ServerName",
    "addresses": [
        "8.8.8.8", "8.8.4.4", "1.1.1.1"
    ]
}
```

__Response Example:__
```json
{
    "haloName": "ServerName",
    "addresses": [
        "8.8.8.8", "8.8.4.4", "1.1.1.1"
    ]
}
```


## /getHalos
Get all the Halos from The Ark/

__Type:__ `GET`

__Request Parameters:__

None

__Request Example:__
```json
{}
```

__Response Example:__
```json
{
    "halos": [
        "halo1",
        "halo2",
        ...
    ]
}
```


## /deleteHalo
Delete a Halo from The Ark and cleanup all the forwards

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| haloName | string   | no                 | The name of the Halo                           |

__Request Example:__
```json
{
    "haloName": "ServerName"
}
```

__Response Example:__
```json
{
    "haloName": "ServerName"
}
```