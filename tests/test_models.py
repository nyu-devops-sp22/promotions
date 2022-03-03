"""
Test cases for Promotion Model

"""
import logging
import unittest
import os
from service.models import Promotion, Type, DataValidationError, db
from service import app
from datetime import datetime

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestPromotion(unittest.TestCase):
    """ Test Cases for Promotion Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        Promotion.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        """ Create a promotion and assert that it can be instantiated"""
        promo = Promotion(name="Summer Sale", start_date=datetime.now(), type=Type.Percentage, value=0.2, ongoing=False)
        self.assertEqual(promo.name, "Summer Sale")
        self.assertEqual(promo.products, [])
        self.assertTrue(promo is not None)


    def test_add_promotion(self):
        """ Add a promotion to the database """
        promotions = Promotion.all()
        promo = Promotion(name="Summer Sale", start_date=datetime.now(), type=Type.Percentage, value=0.2, ongoing=False)
        self.assertTrue(promo is not None)
        self.assertEqual(promo.id, None)
        promo.create()
        self.assertEqual(promo.id, 1)

    def test_delete_promotion(self):
        """ Delete a Promotion """
        promo = Promotion(name="Summer Sale", start_date=datetime.now(), type=Type.Percentage, value=0.2, ongoing=False)
        promo.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the pet and make sure it isn't in the database
        promo.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_find_promotion_by_name(self):
        """Find a Promotion by Name"""
        Promotion(name="Summer Sale", start_date=datetime.now(), type=Type.Percentage, value=0.2, ongoing=False).create()
        Promotion(name="Winter Sale", start_date=datetime.now(), type=Type.Value, value=10.99, ongoing=True).create()
        prom = Promotion.find_by_name("Summer Sale")
        self.assertEqual(prom[0].type, Type.Percentage)
        self.assertEqual(prom[0].name, "Summer Sale")
        self.assertEqual(len(Promotion.all()), 2)

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)
