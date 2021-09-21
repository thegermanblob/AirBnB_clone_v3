#!/usr/bin/python3
""" Handles all state objects for the api """
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('states/<state_id>/cities/',
                 methods=["GET"], strict_slashes=False)
def city(state_id=None):
    """
    Display the cities listed in alphabetical order
    ---
    responses:
      200:
        description: A list of state dictionaries
        examples:
          states: 
                [
                    {"name":'Cali'},
                    {"name":'Florida'},
                    {"name":'Colorado'},
                ]
    """ 
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_dict = []
    for city in state.cities:
        new_dict.append(city.to_dict())
    return jsonify(new_dict)


@app_views.route('/cities/<city_id>', methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id=None):
    """
    Gets a city by the given city_id 
    ---
    responses:
      200:
        description: A json dictionary of a city
        examples:
                {
                    "name":"Florida", 
                    "id":"lk213jiodsaifulkjewq",
                    "created_at":"09/20/2021",
                }
    """ 
    city = storage.get(City, city_id)
    if city is not None:
        city = city.to_dict()
        return jsonify(city)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id=None):
    """
    Deletes city by given id 
    ---
    response:
      200:
        description: An empty dictionary
        examples: {}
    """
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities/',
                 methods=["POST"], strict_slashes=False)
def post_city(state_id=None):
    """
    Creates given json obj in db with given id 
    ---
    response:
      201:
        description: Successfully creates the city, and returns a dictionary
        example: 
                {
                  "__class__":"City",
                  "created_at":"2021-09-19T13:41:44.000000",
                  "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                  "state_id":"9123f5f3-70c0-4b3a-a9ea-9f12321388",
                  "name":"Alexandria",
                  "updated_at":"2021-09-19T17:41:44.000000"
                 }
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_city_dict = request.get_json()
    if "name" not in new_city_dict.keys():
        return Response("Missing name", status=400)
    new_city_dict['state_id'] = state.id
    instance = City(**new_city_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def put_city(city_id=None):
    """
    Updates a city object with the given id and json
    ---
    response:
      201:
        description: Successfully updated the city, and returns a dictionary
        example:
                {
                    "__class__":"City",
                    "created_at":"2021-09-19T13:41:44.000000",
                    "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                    "state_id":"9123f5f3-70c0-4b3a-a9ea-9f12321388",
                    "name":"Detroit",
                    "updated_at":"2021-09-19T17:41:44.000000"
                }
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_state_dict = request.get_json()
    for key, value in new_state_dict.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
