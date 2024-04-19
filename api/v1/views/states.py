#!/usr/bin/python3
"""
This module handles all routes with the blueprint app_views
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

State = classes["State"]


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieve all states
    """
    states_list = [
        state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieve a state by id
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Delete state
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create state
    """
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    try:
        name = data['name']
    except KeyError:
        abort(400, 'Missing name')

    state = State(name=name)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update state
    """
    ignored_list = ["id", "created_at", "updated_at"]
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        for key, val in data.items():
            if key not in ignored_list:
                setattr(state, key, val)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict())
    return abort(404)
