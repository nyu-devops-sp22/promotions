"""
Test cases for Promotion Model

"""
import logging
import os
import unittest
from datetime import datetime

from service import app
from service.models import DataValidationError, Promotion, Type, db
from werkzeug.exceptions import NotFound

from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
######################################################################
#  P R O M O T I O N   M O D E L   T E S T   C A S E S
######################################################################


class TestPromotion(unittest.TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Promotion.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        """Create a promotion and assert that it can be instantiated"""
        promo = Promotion(
            name="Summer Sale",
            start_date=datetime.now(),
            type=Type.PERCENTAGE,
            value=0.2,
            ongoing=False,
            product_id=11,
        )
        self.assertEqual(promo.name, "Summer Sale")
        self.assertTrue(promo is not None)

    def test_add_promotion(self):
        """Add a promotion to the database"""
        promotions = Promotion.all()
        promo = Promotion(
            name="Summer Sale",
            start_date=datetime.now(),
            type=Type.PERCENTAGE,
            value=0.2,
            ongoing=False,
            product_id=12,
        )
        self.assertTrue(promo is not None)
        self.assertEqual(promo.id, None)
        promo.create()
        self.assertEqual(promo.id, 1)

    def test_delete_promotion(self):
        """Delete a Promotion"""
        promo = Promotion(
            name="Summer Sale",
            start_date=datetime.now(),
            type=Type.PERCENTAGE,
            value=0.2,
            ongoing=False,
            product_id=11,
        )
        promo.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the pet and make sure it isn't in the database
        promo.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_update_promotion(self):
        """Update a promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.create()
        logging.debug(promotion)
        self.assertEqual(promotion.id, 1)
        # Change it an save it
        promotion.value = 0.2
        promotion_name = "hello"
        promotion.name = promotion_name
        original_id = promotion.id
        promotion.update()
        self.assertEqual(promotion.id, original_id)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change

        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].id, 1)
        self.assertEqual(promotions[0].name, promotion_name)
        self.assertEqual(promotions[0].value, 0.2)

    def test_find_promotion_by_name(self):
        """Find a Promotion by Name"""
        Promotion(
            name="Summer Sale",
            start_date=datetime.now(),
            type=Type.PERCENTAGE,
            value=0.2,
            ongoing=False,
            product_id=11,
        ).create()
        Promotion(
            name="Winter Sale",
            start_date=datetime.now(),
            type=Type.VALUE,
            value=10.99,
            ongoing=True,
            product_id=12,
        ).create()
        prom = Promotion.find_by_name("Summer Sale")
        self.assertEqual(prom[0].type, Type.PERCENTAGE)
        self.assertEqual(prom[0].name, "Summer Sale")
        self.assertEqual(len(Promotion.all()), 2)

    def test_find_by_product_id(self):
        """Find Promotions by product_id"""
        Promotion(
            name="Summer Sale",
            start_date=datetime.now(),
            type=Type.PERCENTAGE,
            value=0.2,
            ongoing=True,
            product_id=11,
        ).create()
        Promotion(
            name="Winter Sale",
            start_date=datetime.now(),
            type=Type.PERCENTAGE,
            value=0.3,
            ongoing=False,
            product_id=12,
        ).create()
        promotions = list(Promotion.find_by_product_id(11))
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].name, "Summer Sale")
        self.assertEqual(promotions[0].value, 0.2)

    def test_serialize_a_promotion(self):
        """Test serialization of a Promotion"""
        promotion = PromotionFactory()
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("start_date", data)
        self.assertEqual(
            data["start_date"], promotion.start_date.strftime("%m-%d-%Y %H:%M:%S %z")
        )
        self.assertIn("end_date", data)
        self.assertEqual(
            data["end_date"], promotion.end_date.strftime("%m-%d-%Y %H:%M:%S %z")
        )
        self.assertIn("type", data)
        self.assertEqual(data["type"], promotion.type.name)
        self.assertIn("value", data)
        self.assertEqual(data["value"], promotion.value)
        self.assertIn("ongoing", data)
        self.assertEqual(data["ongoing"], promotion.ongoing)
        self.assertIn("product_id", data)
        self.assertEqual(data["product_id"], promotion.product_id)

    def test_deserialize_a_promotion(self):
        """Test deserialization of a Promotion"""
        example = PromotionFactory()
        data = example.serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, example.name)
        self.assertEqual(
            promotion.start_date,
            datetime.strptime(data["start_date"], "%m-%d-%Y %H:%M:%S %z"),
        )
        self.assertEqual(
            promotion.end_date,
            datetime.strptime(data["end_date"], "%m-%d-%Y %H:%M:%S %z"),
        )
        self.assertEqual(promotion.type, example.type)
        self.assertEqual(promotion.value, example.value)
        self.assertEqual(promotion.ongoing, example.ongoing)
        self.assertEqual(promotion.product_id, example.product_id)
    
    def test_deserialize_special_promotion(self):
        """Test deserialization of a special Promotion (no end date and value is int)"""
        example = PromotionFactory()
        example.end_date = None
        example.value = 1
        data = example.serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, example.name)
        self.assertEqual(
            promotion.start_date,
            datetime.strptime(data["start_date"], "%m-%d-%Y %H:%M:%S %z"),
        )
        self.assertEqual(promotion.type, example.type)
        self.assertEqual(promotion.value, example.value)
        self.assertEqual(promotion.ongoing, example.ongoing)
        self.assertEqual(promotion.product_id, example.product_id)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_name(self):
        """Test deserialization of bad name attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["name"] = 3.0  # wrong type
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_start_date(self):
        """Test deserialization of bad start_date attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["start_date"] = 2022.03  # wrong type
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_end_date(self):
        """Test deserialization of bad end_date attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["end_date"] = 2022.03  # wrong type
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_type(self):
        """Test deserialization of bad type attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["type"] = 1  # wrong case
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_value(self):
        """Test deserialization of bad value attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["value"] = "Value"  # wrong type
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_ongoing(self):
        """Test deserialization of bad ongoing attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["ongoing"] = "ongoing"  # wrong type
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_product_id(self):
        """Test deserialization of bad product_id attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["product_id"] = 1.0  # wrong type
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_no_end_date(self):
        """Test deserialization of attribute end_date = None"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["end_date"] = None
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertIs(promotion.end_date, None)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Promotion with missing data"""
        data = {
            "start_date": datetime.now(),
            "type": Type.PERCENTAGE,
            "value": 0.2,
            "ongoing": True,
            "product_id": 2,
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_invalid_start_date(self):
        """Test deserialization of a Promotion with invalid start_date data type"""
        data = {
            "name": "Summer Sale",
            "start_date": "202-03-01",
            "type": Type.PERCENTAGE,
            "value": 0.2,
            "ongoing": True,
            "product_id": 2,
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_repr(self):
        """Test representation of a promotion"""
        promotion = PromotionFactory()
        self.assertEqual(
            repr(promotion), "<Promotion %r id=[%s]>" % (promotion.name, promotion.id)
        )

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        promotions = PromotionFactory.create_batch(3)
        for promotion in promotions:
            promotion.create()

        promotion = Promotion.find_or_404(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)
        self.assertEqual(promotion.type, promotions[1].type)
        self.assertEqual(promotion.start_date, promotions[1].start_date)
        self.assertEqual(promotion.end_date, promotions[1].end_date)
        self.assertEqual(promotion.value, promotions[1].value)
        self.assertEqual(promotion.ongoing, promotions[1].ongoing)
        self.assertEqual(promotion.product_id, promotions[1].product_id)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Promotion.find_or_404, 0)
