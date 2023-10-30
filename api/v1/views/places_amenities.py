#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_in_place(place_id):
    """Retrieves the list of all amenities in a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_in_place(place_id, amenity_id):
    """Delete an Amenity in a Place Object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place_amenities = place.amenities
    if amenity not in place_amenities:
        abort(404)
    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    place.save()

    # storage_t = getenv('HBNB_TYPE_STORAGE')
    # if storage_t == 'db':
    #     for one in place.amenities:
    #         if one.id == amenity_id:
    #             amenity = one
    #             break
    #     if not amenity:
    #         abort(404)
    #     storage.delete(amenity)
    # else:
    #     if amenity_id in place.amenity_ids:
    #         amenity = storage.get(Amenity, amenity_id)
    #         storage.delete(amenity)
    #         place.amenity_ids.remove(amenity_id)
    #     else:
    #         abort(404)
    # storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    """Add a Amenity Object to a Place Object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
