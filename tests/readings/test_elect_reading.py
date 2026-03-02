from datetime import date
from decimal import Decimal

import pytest

from src.apps.readings.models import ElectReading
from tests.factory import ElectReadingFactory


@pytest.mark.django_db
def test_with_elect_reading_qty_auto_computed():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_value=200)
    ElectReadingFactory(reading_date=date(2024, 2, 1), reading_value=350)

    qs = ElectReading.objects.with_elect_reading_qty().order_by("reading_date")

    assert qs[0].elect_reading_qty is None  # нет предыдущего значения
    assert qs[1].elect_reading_qty == 150  # 350 - 200


@pytest.mark.django_db
def test_with_elect_reading_qty_manual_override():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_value=200)
    ElectReadingFactory(reading_date=date(2024, 2, 1), reading_value=350, reading_qty=999)

    qs = ElectReading.objects.with_elect_reading_qty().order_by("reading_date")

    assert qs[1].reading_qty == 999  # ручное поле приоритетнее в with_elect_reading_sum через Coalesce


@pytest.mark.django_db
def test_with_elect_reading_sum_multiple_records():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_value=200, unit_price=Decimal("4.32"))
    ElectReadingFactory(reading_date=date(2024, 2, 1), reading_value=350, unit_price=Decimal("5.00"))

    qs = ElectReading.objects.with_elect_reading_sum().order_by("reading_date")

    assert qs[0].total_elect_reading_sum == Decimal("0.00")  # NULL qty → 0
    assert qs[1].total_elect_reading_sum == Decimal("750.00")  # 150 * 5.00


@pytest.mark.django_db
def test_with_elect_reading_sum_with_positive_adj_unit_sum():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_value=200, unit_price=Decimal("4.32"))
    ElectReadingFactory(
        reading_date=date(2024, 2, 1),
        reading_value=400,
        unit_price=Decimal("4.32"),
        adj_unit_sum=Decimal("50.00"),
    )

    result = ElectReading.objects.with_elect_reading_sum().order_by("reading_date")[1]

    assert result.total_elect_reading_sum == Decimal("914.00")  # 200 * 4.32 + 50.00


@pytest.mark.django_db
def test_with_elect_reading_sum_with_negative_adj_unit_sum():
    ElectReadingFactory(reading_date=date(2024, 1, 1), reading_value=200, unit_price=Decimal("4.32"))
    ElectReadingFactory(
        reading_date=date(2024, 2, 1),
        reading_value=400,
        unit_price=Decimal("4.32"),
        adj_unit_sum=Decimal("-50.00"),
    )

    result = ElectReading.objects.with_elect_reading_sum().order_by("reading_date")[1]

    assert result.total_elect_reading_sum == Decimal("814.00")  # 200 * 4.32 - 50.00


@pytest.mark.django_db
def test_str_representation():
    record = ElectReadingFactory(reading_date=date(2024, 3, 1), reading_value=530)

    assert "530" in str(record)
