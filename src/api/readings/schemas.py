import datetime
from decimal import Decimal

from ninja import Schema


class ElectReadingOut(Schema):
    id: int
    reading_date: datetime.date
    reading_value: int
    unit_price: Decimal
    elect_reading_qty: int | None = None
    total_elect_reading_sum: Decimal | None = None


class GasReadingOut(Schema):
    id: int
    reading_date: datetime.date
    real_reading_value: int
    dec_reading_value: int
    dec_real_reading_diff: int
    dec_reading_qty: int
    dec_unit_price: Decimal
    total_dec_reading_sum: Decimal | None = None
    total_trans_sum: Decimal | None = None


class ElectReadingFilters(Schema):
    year: int | None = None
    month: int | None = None
    last: bool = False


class GasReadingFilters(Schema):
    year: int | None = None
    month: int | None = None
    last: bool = False
