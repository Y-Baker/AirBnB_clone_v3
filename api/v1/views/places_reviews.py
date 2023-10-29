#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_in_place(place_id):
    """Retrieves the list of all Reviews in a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review Object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review Object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """Add a Review Object to a Place Object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if not data.get('user_id'):
        abort(400, "Missing user_id")
    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)
    if not data.get('text'):
        abort(400, "Missing text")

    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at',
                       'user_id', 'place_id']:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())
