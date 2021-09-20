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
    """display the city and cities listed in alphabetical order"""
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
    """ gets a city by the given city """
    place = storage.get(Place, place_id)
    if place is not None:
        place = place.to_dict()
        return jsonify(place)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ Deletes state by given id """
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
    """ Creates given json obj in db with given id """
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
    user = storage.get(User, str(new_place_dict["user_id"]))
    if user is None:
        abort(404)
    new_place_dict['city_id'] = city.id
    instance = Place(**new_place_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def put_place(place_id=None):
    """ Updates a state object with the given id and json """
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
