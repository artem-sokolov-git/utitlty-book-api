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
    adj_costs = models.DecimalField(
        verbose_name="Корректировка суммы (UAH)",
        help_text="Сумма корректировки (положительная — доплата, отрицательная — переплата)",
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        abstract = True
