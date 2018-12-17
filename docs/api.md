# The Ark API Documentation
Documentation of all the API functions for The Ark. You can find implementations of these in [api.py](../theark/api.py). You may click on each of the names to see examples and full spec.

## Format
All data to and from the server will be of type `application/json`.
Responses from the server will be one of three status codes:

`200`: The request went through

`400`: Missing or invalid parameters

`403`: Authentication Error. See [authentication](./api-authentication.md) for more details

## API Calls
List of all the API calls

### [/registerServer](./api-servers.md#registerServer)
Register a new `standard` server with The Ark. See [server registration](./api-servers.md) for more information on the types of servers.

### [/registerRedirectServer](./api-servers.md#registerRedirectServer)
Register a new `redirect` server with The Ark. See [server registration](./api-servers.md) for more information on the types of servers.

### [/deleteServer](./api-servers.md#deleteServer)
Delete a server and remove all forwards.

### [/getAddresses](./api-information.md#getAddresses)
Get assigned addreses from The Ark for the given server.

### [/getServerSettings](./api-information.md#getAddresses)
Return the settings that are registered for the server.

### [/getNginxConfig](./api-information.md#getAddresses)
If the server is a `redirect` server, return the NGINX server block that The Ark uses (or would use)
to redirect the traffic.
