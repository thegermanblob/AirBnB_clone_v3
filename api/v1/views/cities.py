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
    """display the city and cities listed in alphabetical order"""
    state = storage.get(State, state_id)
    new_dict = []
    for city in state.cities:
        new_dict.append(city.to_dict())
    return jsonify(new_dict)


@app_views.route('/cities/<city_id>', methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id=None):
    """ gets a city by the given city """
    city = storage.get(City, city_id)
    if city is not None:
        city = city.to_dict()
        return jsonify(city)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id=None):
    """ Deletes state by given id """
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities/', methods=["POST"], strict_slashes=False)
def post_city(state_id=None):
    """ Creates given json obj in db with given id """
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
    """ Updates a state object with the given id and json """
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
