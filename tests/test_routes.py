"""
TestPromotion API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import logging
import os
from unittest import TestCase
# from unittest.mock import MagicMock, patch

from service import app, status  # HTTP Status Codes
from service.models import db, init_db

from .factories import PromotionFactory

logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotionServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """This runs once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    def _create_promotions(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            resp = self.app.post(
                BASE_URL, json=test_promotion.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test promotion"
            )
            new_promotion = resp.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_promotion(self):
        """Get a single Promotion"""
        # get the id of a pet
        test_promotion = self._create_promotions(1)[0]
        resp = self.app.get(
            "/promotions/{}".format(test_promotion.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], test_promotion.name)
        self.assertEqual(data['start_date'].strip(),
                         test_promotion.start_date.strftime("%m-%d-%Y %H:%M:%S %z")[:-5].strip())
        self.assertEqual(data['end_date'].strip(),
                         test_promotion.end_date.strftime("%m-%d-%Y %H:%M:%S %z")[:-5].strip())
        self.assertEqual(data['type'], test_promotion.type.name)
        self.assertEqual(data['value'], test_promotion.value)
        self.assertEqual(data['ongoing'], test_promotion.ongoing)
        self.assertEqual(
            data['product_id'], test_promotion.product_id)

    def test_create_promotion(self):
        """Create a new Promotion"""
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        resp = self.app.post(
            BASE_URL, json=test_promotion.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion['name'],
                         test_promotion.name, "Names do not match")
        self.assertEqual(new_promotion['start_date'].strip(),
                         test_promotion.start_date.strftime("%m-%d-%Y %H:%M:%S %z")[:-5].strip())
        self.assertEqual(new_promotion['end_date'].strip(),
                         test_promotion.end_date.strftime("%m-%d-%Y %H:%M:%S %z")[:-5].strip())
        self.assertEqual(new_promotion['type'], test_promotion.type.name)
        self.assertEqual(new_promotion['value'], test_promotion.value)
        self.assertEqual(new_promotion['ongoing'], test_promotion.ongoing)
        self.assertEqual(
            new_promotion['product_id'], test_promotion.product_id)

        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion['name'],
                         test_promotion.name, "Names do not match")
        self.assertEqual(new_promotion['start_date'].strip(),
                         test_promotion.start_date.strftime("%m-%d-%Y %H:%M:%S %z")[:-5].strip())
        self.assertEqual(new_promotion['end_date'].strip(),
                         test_promotion.end_date.strftime("%m-%d-%Y %H:%M:%S %z")[:-5].strip())
        self.assertEqual(new_promotion['type'], test_promotion.type.name)
        self.assertEqual(new_promotion['value'], test_promotion.value)
        self.assertEqual(new_promotion['ongoing'], test_promotion.ongoing)
        self.assertEqual(
            new_promotion['product_id'], test_promotion.product_id)
