"""
Test Factory to make fake objects for testing
"""
from datetime import datetime, timezone

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyFloat
from service.models import Promotion, Type


class PromotionFactory(factory.Factory):
    """Creates fake promotions"""

    class Meta:
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    start_date = FuzzyDateTime(
        datetime(2022, 1, 1, tzinfo=timezone.utc),
        datetime(2022, 1, 20, 20, tzinfo=timezone.utc),
    )
    end_date = FuzzyDateTime(
        datetime(2022, 1, 21, tzinfo=timezone.utc),
        datetime(2022, 2, 27, tzinfo=timezone.utc),
    )
    type = FuzzyChoice(choices=[Type.VALUE, Type.PERCENTAGE, Type.UNKNOWN])
    value = FuzzyFloat(1.0, 99.0)
    ongoing = FuzzyChoice(choices=[True, False])
    product_id = factory.Sequence(lambda n: n)
