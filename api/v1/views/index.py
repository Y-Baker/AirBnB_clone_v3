#!/usr/bin/python3
"""Module for Add Some route to Flask App"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """return a json say that everything is ok"""
    return jsonify({'status': 'OK'})
