from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value, Window
from django.db.models.functions import Coalesce


class GasReadingQuerySet(models.QuerySet):
    def with_declaration_values(self) -> "GasReadingQuerySet":
        init_dec_reading = settings.GAS_DEC_INITIAL_READING
        return self.annotate(
            real_reading_value=F("reading_value"),
            dec_reading_value=Window(
                expression=Sum("reading_qty"),
                order_by=F("reading_date").asc(),
            )
            + Value(init_dec_reading),
            dec_real_reading_diff=Coalesce(F("reading_value"), 0)
            - (
                Window(
                    expression=Sum("reading_qty"),
                    order_by=F("reading_date").asc(),
                )
                + Value(init_dec_reading)
            ),
            dec_reading_qty=F("reading_qty"),
            dec_unit_price=F("unit_price"),
            total_dec_reading_sum=ExpressionWrapper(
                F("reading_qty") * F("unit_price") + Coalesce(F("adj_unit_sum"), Decimal(0)),
                output_field=DecimalField(),
            ),
        )

    def with_trans_sum(self) -> "GasReadingQuerySet":
        return self.annotate(
            total_trans_sum=ExpressionWrapper(
                Coalesce(F("trans_sum"), Decimal(0)) + Coalesce(F("adj_trans_sum"), Decimal(0)),
                output_field=DecimalField(),
            )
        )
