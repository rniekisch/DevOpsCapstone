from flask import Flask, request
from flask.logging import create_logger
import logging


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    browser = request.headers.get("User-Agent")
    url = request.values.get("url") or request.headers.get("Referer")
    event = request.values.get("event")
    ip_address = request.access_route[0] or request.remote_addr
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
        </table>
    </body>
</html>'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80
