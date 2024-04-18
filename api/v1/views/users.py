#!/usr/bin/python3
"""default RESTFul API actions for State objects"""
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects
    """
    user_list = []
    user_dict = storage.all(User)
    for user in user_dict.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_specific_user(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """
    Creates a user
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
