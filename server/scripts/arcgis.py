import json
import re
from urllib.parse import urlencode
from urllib.request import urlopen


ADDRESS_URL = "http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/geocodeAddresses"


def camel_to_under(s):
    if not s:
        return ""
    return re.sub(r"(?!^)[A-Z]",
                  lambda r: ("_"+r.group(0).lower()),
                  s).lower()


def simplify(result):
    loc = result["location"]
    attrs = result["attributes"]
    return {
        "location": {
            "lng": loc["x"],
            "lat": loc["y"]
        },
        "formatted_name": attrs["Match_addr"],
        "properties": {
            "types": [camel_to_under(attrs["Addr_type"])],
            "score": result["score"]
        }
    }


class ArcGISCoder(object):
    def __init__(self, client_id, client_secret, url=ADDRESS_URL):
        assert client_id and client_secret, \
            "You must supply a client id and secret to ArcGISCoder"

        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.access_token = None

    def get_access_token(self):
        if self.access_token:
            return self.access_token

        data = urlencode([("grant_type", "client_credentials"),
                          ("client_id", self.client_id),
                          ("client_secret", self.client_secret)]).\
                          encode("ISO-8859-1")
        f = urlopen("https://www.arcgis.com/sharing/oauth2/token",
                    data)
        json_response = json.loads(f.read().decode("utf-8"))

        self.access_token = json_response["access_token"]
        return self.access_token

    def geocode(self, addrs, **kwargs):
        if isinstance(addrs, str):
            addrs = [addrs]

        addresses = json.dumps(
            {"records":
             [{"attributes":
               {
                   "OBJECTID": i+1,
                   "Address": addr,
                   "City": "Somerville",
                   "Region": "MA"
               }} for i, addr in enumerate(addrs)]})
        data = {
            "addresses": addresses,
            "token": self.get_access_token(),
            "f": "json"
        }

        f = urlopen(self.url, urlencode(data).encode("ISO-8859-1"))
        result = json.loads(f.read().decode("utf-8"))

        return [simplify(l) for l in result["locations"]]
