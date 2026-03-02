from datetime import date
from decimal import Decimal

import pytest

from src.apps.readings.models import GasReading
from tests.factory import GasReadingFactory


@pytest.mark.django_db
def test_with_gas_reading_value_single(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50)

    result = GasReading.objects.with_declaration_values().get()

    assert result.dec_reading_value == 1050


@pytest.mark.django_db
def test_with_gas_reading_value_cumulative(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50)
    GasReadingFactory(reading_date=date(2024, 2, 1), reading_qty=30)

    qs = GasReading.objects.with_declaration_values().order_by("reading_date")

    assert qs[0].dec_reading_value == 1050  # 50 + 1000
    assert qs[1].dec_reading_value == 1080  # 50 + 30 + 1000


@pytest.mark.django_db
def test_with_gas_reading_value_ordered_by_date(settings):
    settings.GAS_DEC_INITIAL_READING = 0
    GasReadingFactory(reading_date=date(2024, 3, 1), reading_qty=20)
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=10)

    qs = GasReading.objects.with_declaration_values().order_by("reading_date")

    assert qs[0].dec_reading_value == 10  # January — first in the window
    assert qs[1].dec_reading_value == 30  # March — 10 + 20


@pytest.mark.django_db
def test_with_dec_real_reading_diff(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50, reading_value=1080)

    result = GasReading.objects.with_declaration_values().get()

    # dec_reading_value = 50 + 1000 = 1050
    # dec_real_reading_diff = 1080 - 1050 = 30
    assert result.dec_real_reading_diff == 30


@pytest.mark.django_db
def test_with_dec_real_reading_diff_negative(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=50, reading_value=1040)

    result = GasReading.objects.with_declaration_values().get()

    assert result.dec_real_reading_diff == -10  # 1040 - 1050


@pytest.mark.django_db
def test_with_total_dec_reading_sum():
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=10, unit_price=Decimal("7.50"))

    result = GasReading.objects.with_declaration_values().get()

    assert result.total_dec_reading_sum == Decimal("75.00")


@pytest.mark.django_db
def test_with_total_dec_reading_sum_multiple_records():
    GasReadingFactory(reading_date=date(2024, 1, 1), reading_qty=10, unit_price=Decimal("7.50"))
    GasReadingFactory(reading_date=date(2024, 2, 1), reading_qty=20, unit_price=Decimal("8.00"))

    qs = GasReading.objects.with_declaration_values().order_by("reading_date")

    assert qs[0].total_dec_reading_sum == Decimal("75.00")  # 10 * 7.50
    assert qs[1].total_dec_reading_sum == Decimal("160.00")  # 20 * 8.00


@pytest.mark.django_db
def test_with_total_dec_reading_sum_with_positive_adj_unit_sum():
    GasReadingFactory(
        reading_date=date(2024, 1, 1),
        reading_qty=10,
        unit_price=Decimal("7.50"),
        adj_unit_sum=Decimal("20.00"),
    )

    result = GasReading.objects.with_declaration_values().get()

    assert result.total_dec_reading_sum == Decimal("95.00")  # 10 * 7.50 + 20.00


@pytest.mark.django_db
def test_with_total_dec_reading_sum_with_negative_adj_unit_sum():
    GasReadingFactory(
        reading_date=date(2024, 1, 1),
        reading_qty=10,
        unit_price=Decimal("7.50"),
        adj_unit_sum=Decimal("-20.00"),
    )

    result = GasReading.objects.with_declaration_values().get()

    assert result.total_dec_reading_sum == Decimal("55.00")  # 10 * 7.50 - 20.00


@pytest.mark.django_db
def test_gas_reading_default_adj_trans_sum():
    reading = GasReadingFactory(reading_date=date(2024, 1, 1))

    assert reading.adj_trans_sum == Decimal("0")


@pytest.mark.django_db
def test_gas_reading_positive_adj_trans_sum():
    reading = GasReadingFactory(reading_date=date(2024, 1, 1), adj_trans_sum=Decimal("15.00"))

    assert reading.adj_trans_sum == Decimal("15.00")


@pytest.mark.django_db
def test_gas_reading_negative_adj_trans_sum():
    reading = GasReadingFactory(reading_date=date(2024, 1, 1), adj_trans_sum=Decimal("-10.00"))

    assert reading.adj_trans_sum == Decimal("-10.00")


@pytest.mark.django_db
def test_queryset_chaining(settings):
    settings.GAS_DEC_INITIAL_READING = 1000
    GasReadingFactory(
        reading_date=date(2024, 1, 1),
        reading_qty=50,
        reading_value=1060,
        unit_price=Decimal("7.50"),
    )

    result = GasReading.objects.with_declaration_values().get()

    assert result.dec_reading_value == 1050
    assert result.dec_real_reading_diff == 10  # 1060 - 1050
    assert result.total_dec_reading_sum == Decimal("375.00")  # 50 * 7.50
