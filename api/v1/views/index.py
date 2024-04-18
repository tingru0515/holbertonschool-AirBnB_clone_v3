#!/usr/bin/python3
"""The index file"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON response with status OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns the number of each object"""
    types = {'amenities': 'Amenity',
             'cities': 'City',
             'places': 'Place',
             'reviews': 'Review',
             'states': 'State',
             'users': 'User'
             }
    stats = {}
    for key, type in types.items():
        stats[key] = storage.count(type)
    return jsonify(stats)
