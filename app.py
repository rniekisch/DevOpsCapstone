from flask import Flask, request, jsonify
from flask.logging import create_logger
from json import loads
from re import compile, VERBOSE
from urllib import urlopen
import logging

FREE_GEOIP_URL = "http://freegeoip.net/json/{}"
VALID_IP = compile(r"""
\b
(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\b
""", VERBOSE)

def get_geodata(ip):
    """
    Search for geolocation information using http://freegeoip.net/
    """
    if not VALID_IP.match(ip):
        raise ValueError('Invalid IPv4 format')

    url = FREE_GEOIP_URL.format(ip)
    data = {}

    try:
        response = urlopen(url).read()
        data = loads(response)
    except Exception:
        pass

    return data


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    browser = request.headers.get("User-Agent")
    url = request.values.get("url") or request.headers.get("Referer")
    event = request.values.get("event")
    ip_address = request.access_route[0] or request.remote_addr
    geodata = get_geodata(ip_address)
    location = "{}, {}".format(geodata.get("city"),
                               geodata.get("zipcode"))
    return '''
<html>
    <head>
        <title>Visitor Information</title>
    </head>
    <body>
        <table>
            <tr> <td>Browser:</td> <td>'''+browser+'''</td> </tr>
            <tr> <td>Url:</td> <td>'''+url+'''</td> </tr>
            <tr> <td>Event:</td> <td>'''+event+'''</td> </tr>
            <tr> <td>IP Adress:</td> <td>'''+ip_address+'''</td> </tr>
            <tr> <td>Geodata:</td> <td>'''+geodata+'''</td> </tr>
            <tr> <td>Location:</td> <td>'''+location+'''</td> </tr>
        </table>
    </body>
</html>'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80
