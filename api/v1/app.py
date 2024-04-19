#!/usr/bin/python3
"""
This module provides flask app routing certain view pages.
"""
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the storage."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Return a JSON response indicating that
    the endpoint was not found
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.register_blueprint(app_views)
    app.run(host='0.0.0.0', port=5000, threaded=True)
