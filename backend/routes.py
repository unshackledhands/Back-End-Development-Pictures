from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture not found"}, 404
    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    is_already_exists = False
    if not new_picture:
        return {"message": "Invalid input parameter"}, 422
    for picture in data:
        if picture['id'] == new_picture['id']:
            is_already_exists = True
    if is_already_exists:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    try:
        data.append(new_picture)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": f"{new_picture['id']}"}, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json
    for picture in data:
        if picture['id'] == new_picture['id']:
            picture = new_picture
            return {"message": "Picture updated"}, 200
    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    idx_to_delete = None

    for idx, picture in enumerate(data):
        if picture['id'] == id:
            idx_to_delete = idx

    if idx_to_delete is not None:
        del data[idx_to_delete]      
        return {}, 204
    return {"message": "picture not found"}, 404