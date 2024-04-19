#!/usr/bin/python3
"""
This module handles user routes with the blueprint app_views
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

User = classes["User"]


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieve all users
    """
    users_list = [
        user.to_dict() for user in storage.all(User).values()]
    return jsonify(users_list)


@app_views.route(
    '/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieve a user by id
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
    '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete user
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create user
    """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
    '/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update user
    """
    ignored_list = ["id", "created_at", "updated_at"]
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        for key, val in data.items():
            if key not in ignored_list:
                setattr(user, key, val)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict())
    return abort(404)
