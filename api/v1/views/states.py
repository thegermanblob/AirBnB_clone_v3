#!/usr/bin/python3
""" Handles all state objects for the api """
import re
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/', methods=["GET"], strict_slashes=False)
def states():
    """
    Display the states listed in alphabetical order
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
    states = storage.all(State)
    new_dict = []
    for state in states:
        new_dict.append(states[state].to_dict())
    return jsonify(new_dict)


@app_views.route('/states/<state_id>', methods=["GET"],
                 strict_slashes=False)
def state_by_id(state_id=None):
    """
    Gets a state by the given state_id 
    ---
    responses:
      200:
        description: A json dictionary of a state
        examples: 
                {
                    "name":"Florida",
                    "id":"lk213jiodsaifulkjewq",
                    "created_at":"09/20/2021",
                }
    """

    state = storage.get(State, state_id)
    if state is not None:
        state = state.to_dict()
        return jsonify(state)
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id=None):
    """
    Deletes state by given id 
    ---
    response:
      200:
        description: An empty dictionary
        examples: {}
    """
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/', methods=["POST"], strict_slashes=False)
def post_state():
    """
    Creates given json obj in db with given id 
    ---
    response:
      201:
        description: Successfully creates the state,and returns a dictionary
        example: {
                  "__class__":"State",
                  "created_at":"2021-09-19T13:41:44.000000",
                  "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                  "name":"California",
                  "updated_at":"2021-09-19T17:41:44.000000"
                 }
    """
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_state_dict = request.get_json()
    if "name" not in new_state_dict.keys():
        return Response("Missing name", status=400)
    instance = State(**new_state_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def put_state(state_id=None):
    """
    Updates a state object with the given id and json
    ---
    response:
      201:
        description: Successfully updated the state, and returns a dictionary
        example:
                {
                    "__class__":"State",
                    "created_at":"2021-09-19T13:41:44.000000",
                    "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                    "name":"California",
                    "updated_at":"2021-09-19T17:41:44.000000"
                }
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_state_dict = request.get_json()
    for key, value in new_state_dict.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
