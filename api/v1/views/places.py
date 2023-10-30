#!/usr/bin/python3
"""module to describe the view of the place resource"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """list all places in a city in storage"""
    return jsonify(list(map(lambda place: place.to_dict(),
                            storage.get_places_by_city_id(city_id))))


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """list a place from storage"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """list all places in a city in storage"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create a place from storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    if not data.get('name'):
        abort(400, 'Missing name')
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place from storage"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    dc = {k: v for k, v in data.items()
          if k not in ['id', 'created_at',
                       'updated_at', 'user_id', 'city_id']}
    place_dict = place.to_dict()
    place_dict.update(dc)
    place.save()
    return jsonify(place.to_dict()), 200
