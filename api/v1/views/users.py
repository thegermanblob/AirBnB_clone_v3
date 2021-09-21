#!/usr/bin/python3
""" Handles all state objects for the api """
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users/', methods=["GET"], strict_slashes=False)
def users():
    """
    Display the users listed in alphabetical order
    ---
    responses:
      200:
        description: A list of user dictionaries
        examples:
          states: 
                [
                    {
                        "name":'User_1',
                        "id":"lk213jiodsaifulkjewq",
                        "email":"useremaitl@mail.com",                       
                    },
                    {
                        "name":'User_2',
                        "id":"lk213jiodsaifulkjewq",
                        "email":"user2maitl@mail.com",                       
                    },
                    {
                        "name":'User_3',
                        "id":"lk213jiodsaifulkjewq",
                        "email":"user3maitl@mail.com",                       
                    },
                ]
    """
    users = storage.all(User)
    new_dict = []
    for user in users:
        new_dict.append(users[user].to_dict())
    return jsonify(new_dict)


@app_views.route('/users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def user_by_id(user_id=None):
    """
    Gets a user by the given user_id 
    ---
    responses:
      200:
        description: A json dictionary of a user
        examples:
                {
                    "name":"user1", 
                    "id":"lk213jiodsaifulkjewq",
                    "created_at":"09/20/2021",
                    "email":"user1maitl@mail.com",                       
                }
    """
    user = storage.get(User, user_id)
    if user is not None:
        user = user.to_dict()
        return jsonify(user)
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    Deletes user by given id 
    ---
    response:
      200:
        description: An empty dictionary
        examples: {}
    """
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/users/', methods=["POST"], strict_slashes=False)
def post_user():
    """
    Creates given json obj in db with given id 
    ---
    response:
      201:
        description: Successfully creates the user, and returns a dictionary
        example:
                {
                  "__class__":"User",
                  "created_at":"2021-09-19T13:41:44.000000",
                  "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                  "name":"Bob",
                  "email":"bobsemail@bobsemailservice.com",
                  "updated_at":"2021-09-19T17:41:44.000000",
                 }
    """
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


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def put_user(user_id=None):
    """
    Updates a user object with the given id and json
    ---
    response:
      201:
        description: Successfully updated the city, and returns a dictionary
        example:
                {
                  "__class__":"User",
                  "created_at":"2021-09-19T13:41:44.000000",
                  "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                  "name":"Bob",
                  "email":"bobsemail@bobsemailservice.com",
                  "updated_at":"2021-09-19T17:41:44.000000",
                }
    """ 
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
