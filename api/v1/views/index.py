#!/usr/bin/python3
"""
This module handles all routes with the blueprint app_views
"""
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status OK."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    obj = {}
    for cls in classes.values():
        cls_count = storage.count(cls)
        cls_name = cls.__tablename__
        obj[cls_name] = cls_count
    return jsonify(obj)
