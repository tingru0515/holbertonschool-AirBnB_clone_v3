#!/usr/bin/python3
"""
This module handles user routes with the blueprint app_views
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

Review = classes["Review"]
Place = classes["Place"]
User = classes["User"]


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews_by_user(place_id):
    """
    Retrieve all reviews by user
    """
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    abort(404)


@app_views.route(
    '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieve a review by id
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Delete review
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Create review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')

    review = Review(**data, place_id=place.id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Update review
    """
    ignored_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        for key, val in data.items():
            if key not in ignored_list:
                setattr(review, key, val)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict())
    return abort(404)
