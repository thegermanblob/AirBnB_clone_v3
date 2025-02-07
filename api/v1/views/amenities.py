#!/usr/bin/python3
""" Handles all amenity objects for the api """
import re
from flask import jsonify, abort, request, Response
from sqlalchemy.sql.expression import insert
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities/', methods=["GET"], strict_slashes=False)
def amenities():
    """display the amenities listed in alphabetical order
    ---
    responses:
      200:
        description: A list of amenities dictionaries
        examples:
          states: [{"name":'wifi'}, {"name":'bathrooms'}, {"name":'pool'}]
    """
    amenities = storage.all(Amenity)
    new_dict = []
    for amenity in amenities:
        new_dict.append(amenities[amenity].to_dict())
    return jsonify(new_dict)


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id=None):
    """ gets a amenity by the given amenity_id 
    ---
    responses:
      200:
        description: A json dictionary of an amenity
        examples:
          states: [{"name":'wifi'}]
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        amenity = amenity.to_dict()
        return jsonify(amenity)
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ Deletes amenity by given id
    ---
    response:
      200:
        description: An empty dictionary
        examples: {}
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/amenities/', methods=["POST"], strict_slashes=False)
def post_amenity():
    """ Creates given json obj in db with given id 
    ---
    response:
      201:
        description: Successfully creates the amenity,and returns a dictionary
        example: {
                  "__class__":"Amenity",
                  "created_at":"2021-09-19T13:41:44.000000",
                  "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                  "name":"wi-fi",
                  "updated_at":"2021-09-19T17:41:44.000000"
                 }
    """
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_amenity_dict = request.get_json()
    if "name" not in new_amenity_dict.keys():
        return Response("Missing name", status=400)
    instance = Amenity(**new_amenity_dict)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """ Updates a amenity object with the given id and json
    ---
    response:
      201:
           description: Successfully updated the amenity, and returns a dictionary
           example: {
                      "__class__":"Amenity",
                      "created_at":"2021-09-19T13:41:44.000000",
                      "id":"9605f5f3-70c0-4b3a-a9ea-9f72c5773f88",
                      "name":"Wi-fi",
                      "updated_at":"2021-09-19T17:41:44.000000"
                    }
    """ 
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.is_json is False:
        return Response("Not a JSON", status=400)
    new_amenity_dict = request.get_json()
    for key, value in new_amenity_dict.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
