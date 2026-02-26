from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F
from django.db.models.functions import Coalesce


class BaseReadingQuerySet(models.QuerySet):
    costs_field: str

    def with_costs(self) -> "BaseReadingQuerySet":
        return self.annotate(
            **{
                self.costs_field: ExpressionWrapper(
                    Coalesce(F("reading_qty"), 0) * Coalesce(F("unit_price"), Decimal(0)),
                    output_field=DecimalField(),
                )
            }
        )
