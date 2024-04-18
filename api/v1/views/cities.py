#!/usr/bin/python3
"""
States file
"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def state_cities(state_id):
    """
    Retrieves the list of City objects of a State
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = state.cities
    cities_dict_list = []
    for city in cities_list:
        cities_dict_list.append(city.to_dict())
    return jsonify(cities_dict_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """
    Creates a city
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
    Updates a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
