"""
Models for Promotion

All of the models are stored in this module

Models
------
Promotion - A Promotion used in the e-commerce service

Attributes:
-----------
id (int) - the id of the promotion
name (string) - the name of the promotion
code (string) - the code that identifies the promotion
start_date (datetime) - the date the promotion starts
end_date (datetime) - the date the promotion ends (can be null)
type - the promotion type (value off, percentage off etc.)
value (number) - the discounted value the promotion applies to products
ongoing (boolean) - True for promotions that are ongoing
product_id (Integer) - product id that's part of the promotion 

"""
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    Promotion.init_db(app)

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Type(Enum):
    """Enumeration of valid Promotion Types"""

    Value = 0 # $10 off, $20 off etc.
    Percentage = 1 # 10% off, 20% off etc.
    Unknown = 3


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """

    ##################################################
    # Table Schema
    ##################################################

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)  # the name of the promotion
    start_date = db.Column(db.DateTime, nullable=False)  # the date the promotion starts
    end_date = db.Column(db.DateTime, nullable=True)  # the date the promotion ends (can be null)
    type =  db.Column(db.Enum(Type), nullable=False)  # the promotion type (value off, percentage off etc.)
    value = db.Column(db.Float, nullable=False)  # the discounted value the promotion applies to products
    ongoing = db.Column(db.Boolean, nullable=False)  # True for promotions that are ongoing
    product_id = db.Column(db.Integer) 
    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Promotion %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Promotion to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Promotion to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Promotion from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Promotion into a dictionary """
        return {"id": self.id, "name": self.name}

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotion: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotion: body of request contained bad or no data"
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Promotions in the database """
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Promotion by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Promotion by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
