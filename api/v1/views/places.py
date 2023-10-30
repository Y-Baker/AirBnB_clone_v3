#!/usr/bin/python3
"""module to describe the view of the place resource"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """list all places in a city in storage"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]

    return jsonify(places_list)


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
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, k, v)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_place():
    """retrieves all Place objects depending of the JSON request"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    states = [storage.get(State, id) for id in data.get('states', [])]
    cities = [storage.get(City, id) for id in data.get('cities', [])]
    amenities = [storage.get(Amenity, id) for id in data.get('amenities', [])]

    if data == {} or (states == [] and cities == [] and amenities == []):
        places = storage.all(Place).values()
        if places is None:
            places_list = []
        else:
            places_list = [place.to_dict() for place in places]
        return jsonify(places_list)

    cities_search = []
    if states != []:
        for state in states:
            cities_search.extend(state.cities)
    if cities != []:
        for city in cities:
            cities_search.append(city)

    places = []
    for city in cities_search:
        places.extend([place for place in city.places])

    if amenities != []:
        for place in places:
            if amenities not in place.amenities:
                places.remove(place)

    return jsonify([place.to_dict() for place in places])
