# API: Server Registration
API functions for server registration. There are two types of servers in The Ark, `default` and `redirect`.

__default servers__: Default servers request reservation of Ark IP addresses, however, The Ark does nothing else with these IPs.

__redirect servers__: For redirect servers, The Ark will reserve IP addresses, claim the IP addresses, and setup forwarders for the specified ports of the IP.

## /registerServer
Register a new `default` server with The Ark, The Ark will then return a list of the IP
addresses that are assigned to it.

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| name   | string   | no                 | The name of the server                         |
| count  | integer  | yes (15)           | The number of IP addresses to reserve (max 50) |

__Request Example:__
```json
{
    "name": "ServerName",
    "count": 20
}
```

__Response Example:__
```json
{
    "name": "ServerName",
    "addresses": [
        "8.8.8.8", "8.8.4.4", "1.1.1.1"
    ]
}
```


## /registerRedirectServer
Register a new `redirect` server with The Ark, The Ark will then return a list of the IP
addresses that are assigned to it. You may specify two different types of redirect servers,
`http` and `tcp`.
TCP redirect servers will forward all traffic through the given ports. HTTP will forward the
given path to the web URL.

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| name     | string   | no                 | The name of the server                         |
| count    | integer  | yes (15)           | The number of IP addresses to reserve (max 50) |
| reserve  | bool     | yes (yes)          | Whether or not TheArk should reserve these ips |
| tcp      | dict     | yes (none)         | The TCP forward settings for the server        |
| http     | dict     | yes (none)         | The HTTP forward settings for the server       |

__Request Example:__
```json
{
    "name": "ServerName",
    "count": 20,
    "reserve": true,
    "tcp": {
        "server": "10.80.100.1",
        "ports": [
            22, 443, 4444
        ]
    },
    "http": {
        "server": "http://misconfiguration.party/",
        "path": "/"
    }
}
```

__Response Example:__
```json
{
    "name": "ServerName",
    "addresses": [
        "8.8.8.8", "8.8.4.4", "1.1.1.1"
    ]
}
```


## /deleteServer
Delete a server from The Ark and cleanup all the forwards

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| name   | string   | no                 | The name of the server                         |

__Request Example:__
```json
{
    "name": "ServerName",
}
```

__Response Example:__
```json
{
    "name": "ServerName",
}
```