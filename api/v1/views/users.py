#!/usr/bin/python3
"""new view for user resource for all common rest API"""

from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.get('/users', strict_slashes=False)
def get_users():
    """reterive all users from storage
    """
    return jsonify(list(map(lambda user:
                        user.to_dict(), storage.all(User).values())))


@app_views.get('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """reterive user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.delete('/users/<user_id>', strict_slashes=False)
def delete_users(user_id):
    """delete user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.post('/users', strict_slashes=False)
def create_users():
    """post user to storage
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if not data.get('email'):
        abort(400, "Missing email")

    if not data.get('password'):
        abort(400, "Missing password")

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.put('/users/<user_id>', strict_slashes=False)
def update_user(user_id):
    """update user to storage
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    dc = {k: v for k, v in data.items()
          if k not in ['id', 'updated_at', 'created_at']}
    user_dict = user.to_dict()
    user_dict.update(dc)
    user.save()
    return jsonify(user_dict)
