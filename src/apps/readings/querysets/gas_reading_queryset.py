from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value, Window
from django.db.models.functions import Coalesce


class DeclaredGasReadingQuerySet(models.QuerySet):
    def with_readings(self) -> "DeclaredGasReadingQuerySet":
        return self.annotate(
            gas_dec_reading=Window(
                expression=Sum(Coalesce("reading_qty", 0)),
                order_by=F("reading_date").asc(),
            )
            + Value(settings.GAS_DEC_INITIAL_READING)
        )

    def with_diff(self) -> "DeclaredGasReadingQuerySet":
        return self.annotate(
            gas_dec_diff=Coalesce(F("reading_value"), 0) - F("gas_dec_reading"),
        )

    def with_costs(self) -> "DeclaredGasReadingQuerySet":
        return self.annotate(
            gas_dec_sum=ExpressionWrapper(
                Coalesce(F("reading_qty"), 0) * Coalesce(F("unit_price"), Decimal(0)),
                output_field=DecimalField(),
            ),
        )
