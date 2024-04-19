#!/usr/bin/python3
"""
This module handles amenity routes with the blueprint app_views
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

Amenity = classes["Amenity"]


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    Retrieve all amenities
    """
    amenities_list = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities_list)


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieve a amenity by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create amenity
    """
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    try:
        name = data['name']
    except KeyError:
        abort(400, 'Missing name')

    amenity = Amenity(name=name)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update amenity
    """
    ignored_list = ["id", "created_at", "updated_at"]
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        for key, val in data.items():
            if key not in ignored_list:
                setattr(amenity, key, val)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict())
    return abort(404)
