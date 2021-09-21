#!/usr/bin/python3
""" Handles all state objects for the api """
from models.user import User
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.city import City
from models.state import State
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def place(city_id=None):
    """
    Display the places of a given city, listed in alphabetical order
    ---
    responses:
      200:
        description: A list of all place dictionaries in the city
        examples:
          states: 
                [
                    {"name":'A morgue'},
                    {"name":'The small house'},
                    {"name":'My big house'},
                ]
    """ 
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    new_dict = []
    for place in city.places:
        new_dict.append(place.to_dict())
    return jsonify(new_dict)


@app_views.route('/places/<place_id>', methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id=None):
    """
    Gets a place by the given place_id 
    ---
    responses:
      200:
        description: A json dictionary of a place
        examples:
                {
                    "name":"Big house", 
                    "id":"iojewklfdscoielkjfdsm",
                    "city_id":"lk213jiodsaifulkjewq",
                    "created_at":"09/20/2021",
                }
    """
    place = storage.get(Place, place_id)
    if place is not None:
        place = place.to_dict()
        return jsonify(place)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    Deletes place by given id 
    ---
    response:
      200:
        description: An empty dictionary
        examples: {}
    """
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places/',
                 methods=["POST"], strict_slashes=False)
def post_place(city_id=None):
    """
    Creates given json obj in db with given id 
    ---
    response:
      201:
        description: Successfully creates the place, and returns a dictionary
        example: {
                  "__class__":"Place",
                  "created_at":"2021-09-19T13:41:44.000000",
                  "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                  "city_id":"9123f5f3-70c0-4b3a-a9ea-9f12321388",
                  "name":"Big house",
                  "updated_at":"2021-09-19T17:41:44.000000"
                 }
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_place_dict = request.get_json()
    keys = new_place_dict.keys()
    if "name" not in keys:
        return Response("Missing name", status=400)
    if "user_id" not in keys:
        return Response("Missing user_id", status=400)
    user = storage.get(User, new_place_dict.get("user_id"))
    if user is None:
        abort(404)
    new_place_dict['city_id'] = city.id
    instance = Place(**new_place_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def put_place(place_id=None):
    """
    Updates a place object with the given id and json
    ---
    response:
      201:
        description: Successfully updated the place, and returns a dictionary
        example:
                {
                    "__class__":"Place",
                    "created_at":"2021-09-19T13:41:44.000000",
                    "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                    "city_id":"9123f5f3-70c0-4b3a-a9ea-9f12321388",
                    "name":"Big house",
                    "updated_at":"2021-09-19T17:41:44.000000"
                }
    """ 
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_place_dict = request.get_json()
    for key, value in new_place_dict.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
