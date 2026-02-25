from datetime import date, timedelta
from decimal import Decimal

import factory

from src.apps.readings.models import GasReading


class GasReadingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GasReading
        django_get_or_create = ("reading_date",)

    reading_value = factory.Sequence(lambda n: 1000 + n * 50)
    reading_date = factory.Sequence(lambda n: date(2024, 1, 1) + timedelta(days=30 * n))
    reading_qty = factory.Sequence(lambda n: 10 + n * 5)
    unit_price = factory.LazyFunction(lambda: Decimal("7.50"))
    trans_cost = factory.LazyFunction(lambda: Decimal("120.00"))
