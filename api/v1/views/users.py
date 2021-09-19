#!/usr/bin/python3
""" Handles all state objects for the api """
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users/', methods=["GET"], strict_slashes=False)
def users():
    """display the states and cities listed in alphabetical order"""
    users = storage.all(User)
    new_dict = []
    for user in users:
        new_dict.append(users[user].to_dict())
    return jsonify(new_dict)


@app_views.route('/users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def user_by_id(user_id=None):
    """ gets a state by the given state_id """
    user = storage.get(User, user_id)
    if user is not None:
        user = user.to_dict()
        return jsonify(user)
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ Deletes state by given id """
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/users/', methods=["POST"], strict_slashes=False)
def post_user():
    """ Creates given json obj in db with given id """
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_user_dict = request.get_json()
    if "email" not in new_user_dict.keys():
        return Response("Missing email", status=400)
    if "password" not in new_user_dict.keys():
        return Response("Missing password", status=400)
    instance = User(**new_user_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/user/<user_id>', methods=["PUT"], strict_slashes=False)
def put_user(user_id=None):
    """ Updates a state object with the given id and json """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_user_dict = request.get_json()
    for key, value in new_user_dict.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
