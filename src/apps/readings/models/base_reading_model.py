from django.db import models
from django.utils.formats import date_format

from src.apps.common.models import TimeBaseModel


class BaseReadingModel(TimeBaseModel):
    reading_date = models.DateField(
        verbose_name="Дата",
        help_text="Дата снятия показания",
        unique=True,
    )
    unit_price = models.DecimalField(
        verbose_name="Цена",
        help_text="Цена за единицу (по умолчанию предыдущее значение)",
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return date_format(self.reading_date, "F Y")

    class Meta:
        abstract = True
