from django.db import models

from src.apps.common.models import TimeBaseModel


class BaseReadingModel(TimeBaseModel):
    reading_date = models.DateField(
        verbose_name="Дата",
        help_text="Дата снятия показания (по умолчанию текущая дата)",
        unique=True,
    )
    unit_price = models.DecimalField(
        verbose_name="Цена (UAH)",
        help_text="Цена за единицу (по умолчанию предыдущее значение)",
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        abstract = True
