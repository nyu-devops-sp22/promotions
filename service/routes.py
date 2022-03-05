"""
Promotions Service

Paths:
------
GET /promotions - Returns a list all of the Promotions
GET /promotions/{id} - Returns the Promotion with a given id number
POST /promotions - creates a new Promotion record in the database
PUT /promotions/{id} - updates a Promotion record in the database
DELETE /promotions/{id} - deletes a Promotion record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Promotion, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Promotions REST API Service",
            version="1.0",
            # The line below generates an error in the tests because the route for list_promotions has not been implemented yet.
            # paths=url_for("list_promotions", _external=True),
        ),
        status.HTTP_200_OK,
    )


@app.route("/promotions/<int:promotion_id>", methods=['GET'])
def get_promotions(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on its id
    """
    app.logger.info("Request for promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if not promotion:
        raise NotFound(
            "Promotion with id '{}' was not found.".format(promotion_id))

    app.logger.info("Returning promotion: %s", promotion.name)
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)


@app.route("/promotions", methods=['POST'])
def create_promotions():
    """Creates a promotion

    This endpoint will create a Promotion based on the data in the body that is posted
    """
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")
    promotion = Promotion()
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
    location_url = url_for(
        "get_promotions", promotion_id=promotion.id, _external=True)

    app.logger.info("Promotion with ID [%s] created.", promotion.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {'Location': location_url}
    )

@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotions(promotion_id):
    """
    Delete a Promotion
    This endpoint will delete a Promotion based on the id specified in the path
    """
    app.logger.info("Request to delete promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if promotion:
        promotion.delete()

    app.logger.info("Promotion with ID [%s] delete complete.", promotion_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Promotion.init_db(app)
