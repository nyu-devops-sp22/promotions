"""
Test cases for Promotion Model

"""
import unittest
from datetime import datetime

from service import app
from service.models import Promotion, Type, db
from .factories import PromotionFactory


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
        promo = Promotion(name="Summer Sale",
                          start_date=datetime.now(),
                          type=Type.Percentage,
                          value=0.2,
                          ongoing=False,
                          product_id=11)
        self.assertEqual(promo.name, "Summer Sale")
        self.assertTrue(promo is not None)

    def test_add_promotion(self):
        """ Add a promotion to the database """
        promotions = Promotion.all()
        promo = Promotion(name="Summer Sale",
                          start_date=datetime.now(),
                          type=Type.Percentage,
                          value=0.2,
                          ongoing=False,
                          product_id=12)
        self.assertTrue(promo is not None)
        self.assertEqual(promo.id, None)
        promo.create()
        self.assertEqual(promo.id, 1)

    def test_delete_promotion(self):
        """ Delete a Promotion """
        promo = Promotion(name="Summer Sale",
                          start_date=datetime.now(),
                          type=Type.Percentage,
                          value=0.2,
                          ongoing=False,
                          product_id=11)
        promo.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the pet and make sure it isn't in the database
        promo.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_find_promotion_by_name(self):
        """Find a Promotion by Name"""
        Promotion(name="Summer Sale",
                  start_date=datetime.now(),
                  type=Type.Percentage,
                  value=0.2,
                  ongoing=False,
                  product_id=11).create()
        Promotion(name="Winter Sale",
                  start_date=datetime.now(),
                  type=Type.Value,
                  value=10.99,
                  ongoing=True,
                  product_id=12).create()
        prom = Promotion.find_by_name("Summer Sale")
        self.assertEqual(prom[0].type, Type.Percentage)
        self.assertEqual(prom[0].name, "Summer Sale")
        self.assertEqual(len(Promotion.all()), 2)

    def test_find_by_product_id(self):
        """Find Promotions by product_id"""
        Promotion(name="Summer Sale",
                  start_date=datetime.now(),
                  type=Type.Percentage,
                  value=0.2,
                  ongoing=True,
                  product_id=11).create()
        Promotion(name="Winter Sale",
                  start_date=datetime.now(),
                  type=Type.Percentage,
                  value=0.3,
                  ongoing=False,
                  product_id=12).create()
        promotions = list(Promotion.find_by_product_id(11))
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].name, "Summer Sale")
        self.assertEqual(promotions[0].value, 0.2)

    def test_serialize_a_promotion(self):
        """Test serialization of a Promotion"""
        promotion = PromotionFactory()
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], promotion.id)
        self.assertIn('name', data)
        self.assertEqual(data['name'], promotion.name)
        self.assertIn('start_date', data)
        self.assertEqual(
            data['start_date'], promotion.start_date.strftime("%m-%d-%Y %H:%M:%S %z"))
        self.assertIn('end_date', data)
        self.assertEqual(data['end_date'],
                         promotion.end_date.strftime("%m-%d-%Y %H:%M:%S %z"))
        self.assertIn('type', data)
        self.assertEqual(data['type'], promotion.type.name)
        self.assertIn('value', data)
        self.assertEqual(data['value'], promotion.value)
        self.assertIn('ongoing', data)
        self.assertEqual(data['ongoing'], promotion.ongoing)
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], promotion.product_id)

    def test_deserialize_a_promotion(self):
        """Test deserialization of a Promotion"""
        example = PromotionFactory()
        data = example.serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, example.name)
        self.assertEqual(promotion.start_date, datetime.strptime(
            data['start_date'], "%m-%d-%Y %H:%M:%S %z"))
        self.assertEqual(promotion.end_date, datetime.strptime(
            data['end_date'], "%m-%d-%Y %H:%M:%S %z"))
        self.assertEqual(promotion.type, example.type)
        self.assertEqual(promotion.value, example.value)
        self.assertEqual(promotion.ongoing, example.ongoing)
        self.assertEqual(promotion.product_id, example.product_id)

    def test_repr(self):
        """Test representation of a promotion"""
        promotion = PromotionFactory()
        self.assertEqual(repr(promotion), "<Promotion %r id=[%s]>" % (
            promotion.name, promotion.id))
