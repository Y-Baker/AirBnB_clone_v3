#!/usr/bin/python3
"""new view for user resource for all common rest API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """reterive all users from storage
    """
    return jsonify(list(map(lambda user:
                        user.to_dict(), storage.all(User).values())))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """reterive user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_users(user_id):
    """delete user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
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


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update user to storage
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict())
