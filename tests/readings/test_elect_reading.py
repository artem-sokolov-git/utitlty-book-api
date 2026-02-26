from datetime import date
from decimal import Decimal

import pytest

from src.apps.readings.models import ElectReading
from tests.factory import ElectReadingFactory


@pytest.mark.django_db
def test_with_elect_sum_single():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_qty=200, unit_price=Decimal("4.32"))

    result = ElectReading.objects.with_costs().get()

    assert result.elect_sum == Decimal("864.00")  # 200 * 4.32


@pytest.mark.django_db
def test_with_elect_sum_multiple_records():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_qty=200, unit_price=Decimal("4.32"))
    ElectReadingFactory(reading_date=date(2024, 2, 1), reading_qty=150, unit_price=Decimal("5.00"))

    qs = ElectReading.objects.with_costs().order_by("reading_date")

    assert qs[0].elect_sum == Decimal("864.00")  # 200 * 4.32
    assert qs[1].elect_sum == Decimal("750.00")  # 150 * 5.00


@pytest.mark.django_db
def test_str_representation():
    record = ElectReadingFactory(reading_date=date(2024, 3, 1), reading_value=530, reading_qty=120)

    assert "530" in str(record)
    assert "120" in str(record)
