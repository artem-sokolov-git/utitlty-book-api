from datetime import date, timedelta
from decimal import Decimal

import factory

from src.apps.readings.models import ElectReading, GasReading


class ElectReadingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ElectReading
        django_get_or_create = ("reading_date",)

    reading_value = factory.Sequence(lambda n: 500 + n * 100)
    reading_date = factory.Sequence(lambda n: date(2024, 1, 1) + timedelta(days=30 * n))
    unit_price = factory.LazyFunction(lambda: Decimal("4.32"))
    adj_unit_sum = factory.LazyFunction(lambda: Decimal("0"))


class GasReadingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GasReading
        django_get_or_create = ("reading_date",)

    reading_value = factory.Sequence(lambda n: 1000 + n * 50)
    reading_date = factory.Sequence(lambda n: date(2024, 1, 1) + timedelta(days=30 * n))
    reading_qty = factory.Sequence(lambda n: 10 + n * 5)
    unit_price = factory.LazyFunction(lambda: Decimal("7.50"))
    trans_sum = factory.LazyFunction(lambda: Decimal("120.00"))
    adj_trans_sum = factory.LazyFunction(lambda: Decimal("0"))
    adj_unit_sum = factory.LazyFunction(lambda: Decimal("0"))
