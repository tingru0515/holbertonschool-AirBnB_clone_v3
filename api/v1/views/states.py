#!/usr/bin/python3
"""default RESTFul API actions for State objects"""
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states_list():
    """Retrieves all State objects list"""
    obj_list = []
    obj_dict = storage.all(State)
    for obj in obj_dict.values():
        obj_list.append(obj.to_dict())
    return jsonify(obj_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
