# API Authentication
To authenticate to The Ark server, first you must send a login request, after sending the login request, add the `auth-token`
key and value to every API request.

## /login
Login with a username and password to The Ark server

__Type:__ `POST`

__Request Parameters:__

| Name     | Type     | Optional (Default) | Description                                    |
|----------|----------|--------------------|------------------------------------------------|
| username | string   | no                 | The username to authenticate with              |
| password | string   | no                 | The password to authenticate with              |

__Request Example:__
```json
{
    "username": "test",
    "password": "test"
}
```

__Response Example:__
```json
{
    "auth-token": "XXXXXXXXXXXX"
}
```