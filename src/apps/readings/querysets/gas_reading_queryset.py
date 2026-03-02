from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value, Window
from django.db.models.functions import Coalesce


class GasReadingQuerySet(models.QuerySet):
    def with_dec_reading(self) -> "GasReadingQuerySet":
        return self.annotate(
            gas_dec_reading=Window(
                expression=Sum("reading_qty"),
                order_by=F("reading_date").asc(),
            )
            + Value(settings.GAS_DEC_INITIAL_READING)
        )

    def with_dec_diff(self) -> "GasReadingQuerySet":
        qs = self if "gas_dec_reading" in self.query.annotations else self.with_dec_reading()
        return qs.annotate(
            gas_dec_diff=Coalesce(F("reading_value"), 0) - F("gas_dec_reading"),
        )

    def with_trans_cost(self) -> "GasReadingQuerySet":
        return self.annotate(
            total_trans_cost=ExpressionWrapper(
                Coalesce(F("trans_cost"), Decimal(0)) + Coalesce(F("adj_trans_cost"), Decimal(0)),
                output_field=DecimalField(),
            )
        )

    def with_dec_sum(self) -> "GasReadingQuerySet":
        return self.annotate(
            gas_dec_sum=ExpressionWrapper(
                F("reading_qty") * F("unit_price") + Coalesce(F("adj_costs"), Decimal(0)),
                output_field=DecimalField(),
            )
        )
