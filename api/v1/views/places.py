#!/usr/bin/python3
"""
This module handles place routes with the blueprint app_views
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

Place = classes["Place"]
City = classes["City"]
User = classes["User"]


@app_views.route(
    'cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places_by_city(city_id):
    """
    Retrieve all places from city
    """
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieve a place by id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Delete place
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Create place
    """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    place = Place(**data, city_id=city.id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Update place
    """
    ignored_list = ["id", "created_at", "updated_at", "city_id"]
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        for key, val in data.items():
            if key not in ignored_list:
                setattr(place, key, val)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict())
    return abort(404)
