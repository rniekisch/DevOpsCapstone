from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    d = dict()
    d['browser'] = request.headers.get("User-Agent")
    d['url'] = request.values.get("url") or request.headers.get("Referer")
    d['event'] = request.values.get("event")
    d['ipaddress'] = request.remote_addr
    return '''
<html>
    <head>
        <title>Visitor Information</title>
    </head>
    <body>
        <table>
            <tr> <td>Browser:</td> <td>{browser}</td> </tr>
            <tr> <td>Url:</td> <td>{url}</td> </tr>
            <tr> <td>Event:</td> <td>{event}</td> </tr>
            <tr> <td>IP Adress:</td> <td>{ipaddress}</td> </tr>
        </table>
    </body>
</html>'''.format(**d)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80
