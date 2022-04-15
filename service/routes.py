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


from flask import abort, jsonify, make_response, request, url_for
from flask_restx import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound

from service.models import Promotion, Type, DataValidationError, DatabaseConnectionError

from . import app, status

CONTENT_TYPE_JSON = "application/json"

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Promotions REST API Service",
            version="1.0",
            # paths=url_for("list_promotions", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Promotions REST API Service',
          description='This is a service for promotions on products in an eshop.',
          default='promotions',
          default_label='Promotions operation',
          doc='/apidocs', # default also could use doc='/apidocs/'
         )

# Define the model so that the docs reflect what can be sent
create_model = api.model('Promotion', {
    'name': fields.String(required=True,
                          description='The name of the Promotion'),
    'start_date': fields.String(required=True,
                              description='The date the Promotion starts'),
    'end_date': fields.String(required=False,
                              description='The date the Promotion ends'),
    'type': fields.String(required=True,
                          enum=Type._member_names_,
                          description='The type of the Promotion'),
    'value': fields.Float(required=True,
                          description='The discouted value the Promotion applies to the products'),
    'ongoing': fields.Boolean(required=True,
                              description='Is the Promotion ongoing?'),
    'product_id': fields.Integer(required=True,
                                 description='The product id of the product the Promotion is applied to')
})

promotion_model = api.inherit(
    'PromotionModel', 
    create_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
promotion_args = reqparse.RequestParser()
promotion_args.add_argument('name', type=str, required=False, help='List Promotions by name')
promotion_args.add_argument('start_date', type=str, required=False, help='List Promotions by start date')
promotion_args.add_argument('product_id', type=str, required=False, help='List Promotions applied to product identified by product_id')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE

######################################################################
#  PATH: /promotions/{id}
######################################################################
@api.route('/promotions/<promotion_id>')
@api.param('promotion_id', 'The Promotion identifier')
class PromotionResource(Resource):
    """
    PromotionResource Class

    Allows the manipulation of a single Promotion
    GET /promotion{id} - Returns a Promotion with the id
    DELETE /promotion{id} - Deletes a Promotion with the id
    PUT /promotion{id} - Updates a Promotion with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A PROMOTION
    #------------------------------------------------------------------
    @api.doc('get_promotions')
    @api.response(404, 'Promotion not found')
    @api.marshal_with(promotion_model)
    def get(self, promotion_id):
        """
        Retrieve a single Promotion

        This endpoint will return a Promotion based on its id
        """
        app.logger.info("Request for promotion with id: %s", promotion_id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, 'Promotion with id [{}] was not found.'.format(promotion_id))

        app.logger.info("Returning promotion: %s", promotion.name)
        return promotion.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A PROMOTION
    #------------------------------------------------------------------
    @api.doc('delete_promotions')
    @api.response(204, 'Promotion deleted')
    def delete(self, promotion_id):
        """
        Delete a Promotion
        
        This endpoint will delete a Promotion based on the id specified in the path
        """
        app.logger.info("Request to delete promotion with id: %s", promotion_id)
        promotion = Promotion.find(promotion_id)
        if promotion:
            promotion.delete()

        app.logger.info("Promotion with ID [%s] delete complete.", promotion_id)
        return "", status.HTTP_204_NO_CONTENT

    #------------------------------------------------------------------
    # UPDATE AN EXISTING PROMOTION
    #------------------------------------------------------------------
    @api.doc('update_promotions')
    @api.response(404, 'Promotion not found')
    @api.expect(promotion_model)
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        """
        Update promotion value
        This endpoint updates the promotion value of a promotion currently stored in database.

        Args:
            promotion_id (int): the id of promotion in integer
        """
        app.logger.info("Request to update promotion with id: %s; ", promotion_id)
        check_content_type(CONTENT_TYPE_JSON)

        promotion: Promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, 'Promotion with id [{}] was not found.'.format(promotion_id))

        data = api.payload
        promotion.deserialize(data)
        promotion.update()
        app.logger.info("Promotion with id {} has been updated.".format(promotion_id))
        message = promotion.serialize()

        return message, status.HTTP_200_OK


######################################################################
#  PATH: /promotions/{id}/invalidate
######################################################################
@api.route('/promotions/<promotion_id>/invalidate')
@api.param('promotion_id', 'The Promotion identifier')
class InvalidateResource(Resource):
    """Invalidate a Promotion"""
    @api.doc('invalidate_promotions')
    @api.response(404, 'Promotion not found')
    def put(self, promotion_id):
        """
        Invalidates a Promotion
        """
        app.logger.info("Invalidate promotion id: %d", promotion_id)
        promotion: Promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, 'Promotion with id [{}] was not found.'.format(promotion_id))
        promotion.ongoing = False
        promotion.update()
        app.logger.info("Promotion with id {} has been invalidated.".format(promotion_id))
        return promotion.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /promotions
######################################################################
@api.route('/promotions', strict_slashes=False)
class PromotionCollection(Resource):
    """ Handles all interactions with collections of Promotions """
    #------------------------------------------------------------------
    # LIST ALL PROMOTIONS
    #------------------------------------------------------------------
    @api.doc('list_promotions')
    @api.expect(promotion_args, validate=True)
    @api.marshal_list_with(promotion_model)
    def get(self):
        """Returns all of the promotions"""
        app.logger.info("Request for promotion list")
        promotions = []
        product_id = request.args.get("product_id")
        name = request.args.get("name")
        start_date = request.args.get("start_date")
        query_date = request.args.get("active_on")
        if product_id:
            promotions = Promotion.find_by_product_id(product_id)
        elif name:
            promotions = Promotion.find_by_name(name)
        elif start_date:
            promotions = Promotion.find_by_start_date(start_date)
        elif query_date:
            promotions = Promotion.find_active(query_date)
        else:
            promotions = Promotion.all()

        results = [promotion.serialize() for promotion in promotions]
        app.logger.info("Returning %d promotions", len(results))
        return results, status.HTTP_200_OK

    #------------------------------------------------------------------
    # ADD A NEW PROMOTION
    #------------------------------------------------------------------
    @api.doc('create_promotions')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(promotion_model, code=201)
    def post(self):
        """Creates a promotion

        This endpoint will create a Promotion based on the data in the body that is posted
        """
        app.logger.info("Request to create a promotion")
        check_content_type("application/json")
        promotion = Promotion()
        promotion.deserialize(api.payload)
        promotion.create()
        message = promotion.serialize()
        location_url = api.url_for(PromotionResource, promotion_id=promotion.id, _external=True)

        app.logger.info("Promotion with ID [%s] created.", promotion.id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

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
    """Initializes the SQLAlchemy app"""
    global app
    Promotion.init_db(app)
