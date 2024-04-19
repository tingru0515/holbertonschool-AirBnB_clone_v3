#!/usr/bin/python3
"""
This module handles city routes with the blueprint app_views
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

City = classes["City"]
State = classes["State"]


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities_by_state(state_id):
    """
    Retrieve all cities from state
    """
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieve a City by id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Delete city
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Create City
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    try:
        name = data['name']
    except KeyError:
        abort(400, 'Missing name')

    city = City(name=name, state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Update City
    """
    ignored_list = ["id", "created_at", "updated_at", "state_id"]
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        for key, val in data.items():
            if key not in ignored_list:
                setattr(city, key, val)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict())
    return abort(404)
