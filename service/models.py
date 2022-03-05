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
from datetime import datetime
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

    Value = 0  # $10 off, $20 off etc.
    Percentage = 1  # 10% off, 20% off etc.
    Unknown = 3


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """

    ##################################################
    # Table Schema
    ##################################################

    id = db.Column(db.Integer, primary_key=True)
    # the name of the promotion
    name = db.Column(db.String(63), nullable=False)
    # the date the promotion starts
    start_date = db.Column(db.DateTime, nullable=False)
    # the date the promotion ends (can be null)
    end_date = db.Column(db.DateTime, nullable=True)
    # the promotion type (value off, percentage off etc.)
    type = db.Column(db.Enum(Type), nullable=False)
    # the discounted value the promotion applies to products
    value = db.Column(db.Float, nullable=False)
    # True for promotions that are ongoing
    ongoing = db.Column(db.Boolean, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

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
        if self.end_date is not None:
            end_date = self.end_date.strftime("%m-%d-%Y %H:%M:%S %z")
        else:
            end_date = None
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.strftime("%m-%d-%Y %H:%M:%S %z"),
            'end_date': end_date,
            'type': self.type.name,
            'value': self.value,
            'ongoing': self.ongoing,
            'product_id': self.product_id,
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            if isinstance(data['name'], str):
                self.name = data['name']
            else:
                raise DataValidationError(
                    "Invalid type for string [name]: "
                    + str(type(data['name']))
                )
            if isinstance(data['start_date'], str):
                self.start_date = datetime.strptime(
                    data['start_date'], "%m-%d-%Y %H:%M:%S %z")
            else:
                raise DataValidationError(
                    "Invalid type for string [start_date]: "
                    + str(type(data['start_date']))
                )
            if isinstance(data['end_date'], str):
                self.end_date = datetime.strptime(
                    data['end_date'], "%m-%d-%Y %H:%M:%S %z")
            elif data['end_date'] is None:
                self.end_date = None
            else:
                raise DataValidationError(
                    "Invalid type for string [end_date]: "
                    + str(type(data['end_date']))
                )
            if isinstance(data['type'], str):
                self.type = getattr(Type, data['type'])
            else:
                raise DataValidationError(
                    "Invalid type for string [type]: "
                    + str(type(data['type']))
                )
            if isinstance(data['value'], float):
                self.value = data['value']
            else:
                raise DataValidationError(
                    "Invalid type for float [value]: "
                    + str(type(data['value']))
                )
            if isinstance(data['ongoing'], bool):
                self.ongoing = data['ongoing']
            else:
                raise DataValidationError(
                    "Invalid type for boolean [ongoing]: "
                    + str(type(data['ongoing']))
                )
            if isinstance(data['product_id'], int):
                self.product_id = data['product_id']
            else:
                raise DataValidationError(
                    "Invalid type for int [product_id]: "
                    + str(type(data['product_id']))
                )
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError(
                "Invalid promotion: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid promotion: body of request contained bad or no data " +
                str(error)
            )
        except ValueError as error:
            raise DataValidationError(
                "Invalid promotion: perhaps provide invalid format of time" +
                str(error)
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

    @classmethod
    def find_by_product_id(cls, product_id):
        """Return all Promotions applied to a product whose id is `product_id`

        Args:
            product_id (int): the id of a product whose corresponding promotions need to be fetched
        """
        logger.info("Processing product_id query for %s ...", product_id)
        return cls.query.filter(cls.product_id == product_id)
