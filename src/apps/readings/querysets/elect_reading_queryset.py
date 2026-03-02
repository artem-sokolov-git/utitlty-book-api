from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, IntegerField, Window
from django.db.models.functions import Coalesce, Lag


class ElectReadingQuerySet(models.QuerySet):
    def with_elect_reading_qty(self) -> "ElectReadingQuerySet":
        return self.annotate(
            _prev_value=Window(
                expression=Lag("reading_value"),
                order_by=F("reading_date").asc(),
            )
        ).annotate(
            elect_reading_qty=ExpressionWrapper(
                F("reading_value") - F("_prev_value"),
                output_field=IntegerField(),
            )
        )

    def with_elect_reading_sum(self) -> "ElectReadingQuerySet":
        return self.with_elect_reading_qty().annotate(
            total_elect_reading_sum=ExpressionWrapper(
                Coalesce(F("reading_qty"), F("elect_reading_qty"), 0) * Coalesce(F("unit_price"), Decimal(0))
                + Coalesce(F("adj_unit_sum"), Decimal(0)),
                output_field=DecimalField(),
            )
        )
