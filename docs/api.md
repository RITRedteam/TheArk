# The Ark API Documentation
Documentation of all the API functions for The Ark. You can find implementations of these in [api.py](../theark/api.py). You may click on each of the names to see examples and full spec.

## Format
All data to and from the server will be of type `application/json`.
Responses from the server will be one of three status codes:

`200`: The request went through, however, if `error` is specified in the JSON, then it will contain the error message.

```json
{
    "error": "Halo name 'ServerName' is already taken"
}
```

`400`: Missing or invalid parameters or invalid type

`403`: Authentication Error. See [authentication](./api-authentication.md) for more details

## API Calls
List of all the API calls

### [/registerHalo](./api-halos.md#registerHalo)
Register a new `standard` Halo with The Ark. See [Halo registration](./api-halos.md) for more information on the types of Halos.

### [/deleteHalo](./api-halos.md#deleteHalo)
Delete a Halo and remove all forwards.

### [/getAddresses](./api-information.md#getAddresses)
Get assigned addreses from The Ark for the given Halo.

### [/getHaloSettings](./api-information.md#getHaloSettings)
Return the settings that are registered for the Halo.

> NOT IMPLEMENTED, Probably will be deprecated


### [/getNginxConfig](./api-information.md#getNginxConfig)
If the Halo is a `redirect` Halo, return the NGINX Halo block that The Ark uses (or would use)
to redirect the traffic.

> NOT IMPLEMENTED, Probably will be deprecated
