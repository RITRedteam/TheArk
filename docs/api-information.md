# API: Getting Information
API functions for requesting information from the server.

## /getAddresses
Get assigned addreses from The Ark for the given server. You may specify a count in which the server will return `count`
number of random addresses from the pool, this is useful for getting a random IP address to use from The Ark.
If no `count` is specified, or `count` is < 1, The Ark will return all of the addresses.

__Type:__ `GET`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
|  name    | string   | no                 | The name of the server                         |
|  count   | integer  | yes (-1)           | The number of IP addresses to query from The Ark |

__Request Example:__
```json
{
    "name": "ServerName",
    "count": 1
}
```

__Response Example:__
```json
{
    "name": "ServerName",
    "addresses": [
        "1.1.1.1"
    ]
}
```


## /getServerSettings
Return the settings that are registered for the server. Basically, this request will return
the json that was sent during the `/registerServer` call.

__Type:__ `GET`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
|   name   | string   | no                 | The name of the server                         |

__Request Example:__
```json
{
    "name": "ServerName"
}
```

__Response Example:__
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


## /getNginxConfig
If the server is a `redirect` server, return the NGINX server block that The Ark uses (or would use)
to redirect the traffic. This can be useful if you want to host redirectors on multiple boxes.

> Note: If the server is not a Redirect server, the response will not contain an NGINX section.

__Type:__ `GET`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| name     | string   | no                 | The name of the server                         |

__Request Example:__
```json
{
    "name": "ServerName"
}
```

__Response Example:__
```json
{
    "name": "ServerName",
    "NGINX": "stream {\n  server {\n    listen 8.8.8.8:22;\n    proxy_pass 10.80.100.1:22;\n  }\n}"
}
```