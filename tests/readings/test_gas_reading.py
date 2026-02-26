from datetime import date
from decimal import Decimal

import pytest

from src.apps.readings.models import GasReading
from tests.factory import GasReadingFactory


@pytest.mark.django_db
def test_with_gas_dec_reading_single(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50)

    result = GasReading.objects.with_readings().get()

    assert result.gas_dec_reading == 1050


@pytest.mark.django_db
def test_with_gas_dec_reading_cumulative(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50)
    GasReadingFactory(reading_date=date(2024, 2, 1), reading_qty=30)

    qs = GasReading.objects.with_readings().order_by("reading_date")

    assert qs[0].gas_dec_reading == 1050  # 50 + 1000
    assert qs[1].gas_dec_reading == 1080  # 50 + 30 + 1000


@pytest.mark.django_db
def test_with_gas_dec_reading_ordered_by_date(settings):
    settings.GAS_DEC_INITIAL_READING = 0
    GasReadingFactory(reading_date=date(2024, 3, 1), reading_qty=20)
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=10)

    qs = GasReading.objects.with_readings().order_by("reading_date")

    assert qs[0].gas_dec_reading == 10  # January — first in the window
    assert qs[1].gas_dec_reading == 30  # March — 10 + 20


@pytest.mark.django_db
def test_with_gas_dec_diff(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50, reading_value=1080)

    result = GasReading.objects.with_readings().with_diff().get()

    # gas_dec_reading = 50 + 1000 = 1050
    # gas_dec_diff = 1080 - 1050 = 30
    assert result.gas_dec_diff == 30


@pytest.mark.django_db
def test_with_gas_dec_diff_negative(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50, reading_value=1040)

    result = GasReading.objects.with_readings().with_diff().get()

    assert result.gas_dec_diff == -10  # 1040 - 1050


@pytest.mark.django_db
def test_with_gas_dec_sum():
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=10, unit_price=Decimal("7.50"))

    result = GasReading.objects.with_costs().get()

    assert result.gas_dec_sum == Decimal("75.00")


@pytest.mark.django_db
def test_with_gas_dec_sum_multiple_records():
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=10, unit_price=Decimal("7.50"))
    GasReadingFactory(reading_date=date(2024, 2, 1), reading_qty=20, unit_price=Decimal("8.00"))

    qs = GasReading.objects.with_costs().order_by("reading_date")

    assert qs[0].gas_dec_sum == Decimal("75.00")  # 10 * 7.50
    assert qs[1].gas_dec_sum == Decimal("160.00")  # 20 * 8.00


@pytest.mark.django_db
def test_queryset_chaining(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(
        reading_date=date(2024, 1, 1),
        reading_qty=50,
        reading_value=1060,
        unit_price=Decimal("7.50"),
    )

    result = GasReading.objects.with_readings().with_diff().with_costs().get()

    assert result.gas_dec_reading == 1050
    assert result.gas_dec_diff == 10  # 1060 - 1050
    assert result.gas_dec_sum == Decimal("375.00")  # 50 * 7.50
