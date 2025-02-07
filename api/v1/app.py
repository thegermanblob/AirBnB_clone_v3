#!/usr/bin/python3
"""Api for AirBnB_clone"""
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": ["0.0.0.0"]}})


@app.teardown_appcontext
def teardown(exception=None):
    """Application teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception=None):
    """Display an jsonify error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    """Execute api"""
    host = getenv('HBNB_API_HOST')
    if (host is None):
        host = '0.0.0.0'

    port = getenv('HBNB_API_PORT')
    if (port is None):
        port = '5000'

    app.run(host, port, threaded=True)
