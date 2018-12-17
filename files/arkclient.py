import sys
import requests

class ArkApiError(Exception):
    pass

class ArkClient(object):
    def __init__(self, server, username=None, password=None):
        self.server = server.rstrip('/') + "/"
        self.token = None
        if username and password:
            self.login(username, password)

    def _send(self, data):
        """Handle the sending of data to the ark server"""
        endpoint = sys._getframe(1).f_code.co_name  # Calling function name is the endpoint
        if endpoint != "/login" and "auth-token" not in data:
            data['auth-token'] = self.token
        resp = requests.post(self.server+endpoint, json=data)
        if resp.status_code == 200:
            try:
                data = resp.json()
                return data
            except ValueError:
                ArkApiError("Server did not send back valid json")
        elif resp.status_code == 400:
            ArkApiError("An invalid request was sent to the server")
        elif resp.status_code == 403:
            ArkApiError("You are not authorized to call this API function")
        raise ArkApiError("Invald response code: {}".format(resp.status_code))


    def login(self, username, password):
        data = {
            "username": username,
            "password": password
        }
        data = self._send(data)
        if "auth-token" in data:
            self.token = data['auth-token']
            return True
        return False
    
    def registerServer(self, name, count=None):
        """Register a server"""
        data = {
            "name": name
        }
        if count:   data['count'] = count
        return self._send(data)