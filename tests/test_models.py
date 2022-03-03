"""
Test cases for Promotion Model

"""
import logging
import unittest
import os
from service.models import Promotion, Type, Product, DataValidationError, db
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

    def test_create_a_product(self):
        """ Create a product and assert that it can be instantiated"""
        product = Product(name="bicycle", price=99.99, units=100)
        self.assertTrue(product is not None)
        self.assertEqual(product.price, 99.99)
        self.assertEqual(len(product.promotions), 0)

    def test_add_promotion(self):
        """ Add a promotion to the database """
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promo = Promotion(name="Summer Sale", start_date=datetime.now(), type=Type.Percentage, value=0.2, ongoing=False)
        self.assertTrue(promo is not None)
        self.assertEqual(promo.id, None)
        promo.create()
        self.assertEqual(promo.id, 1)

    def test_add_product(self):
        """ Add a product to the database """
        products = Product.all()
        self.assertEqual(products, [])
        prod = Product(name="bicycle", price=99.99, units=100)
        self.assertTrue(prod is not None)
        self.assertEqual(prod.id, None)
        prod.create()
        self.assertEqual(prod.id, 1)

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)
