#!/usr/bin/python3
"""new view for amenity objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.get('/amenities', strict_slashes=False)
def get_amenities():
    """function to get all amenities from storage
    """
    amenities = storage.all(Amenity)
    if amenities is None:
        abort(404)
    return jsonify(list(map
                        (lambda amenity: amenity.to_dict(),
                         amenities.values())))


@app_views.get('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """function to get all amenities from storage
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.delete('/amenities/<amenity_id>', strict_slashes=False)
def delete_amenity(amenity_id):
    """function to delete amenities from storage
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.post('/amenities', strict_slashes=False)
def create_amenity():
    """function to create amenity to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if not data.get('name'):
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.put('/amenities/<amenity_id>', strict_slashes=False)
def update_amenity(amenity_id):
    """function to update amenity to storage
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict())
