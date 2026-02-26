from django.conf import settings
from django.db.models import F, Sum, Value, Window
from django.db.models.functions import Coalesce

from src.apps.readings.querysets.base_reading_queryset import BaseReadingQuerySet


class GasReadingQuerySet(BaseReadingQuerySet):
    costs_field = "gas_dec_sum"

    def with_readings(self) -> "GasReadingQuerySet":
        return self.annotate(
            gas_dec_reading=Window(
                expression=Sum(Coalesce("reading_qty", 0)),
                order_by=F("reading_date").asc(),
            )
            + Value(settings.GAS_DEC_INITIAL_READING)
        )

    def with_diff(self) -> "GasReadingQuerySet":
        return self.annotate(
            gas_dec_diff=Coalesce(F("reading_value"), 0) - F("gas_dec_reading"),
        )
