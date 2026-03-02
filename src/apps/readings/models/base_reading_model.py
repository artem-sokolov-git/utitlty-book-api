from django.db import models

from src.apps.common.models import TimeBaseModel


class BaseReadingModel(TimeBaseModel):
    reading_date = models.DateField(
        verbose_name="Дата",
        help_text="Дата снятия показания",
        unique=True,
    )
    reading_value = models.PositiveIntegerField(
        verbose_name="Показание",
        help_text="Показание на дату снятия",
    )
    reading_qty = models.PositiveIntegerField(
        verbose_name="Потребление",
        help_text="Количество единиц",
        blank=True,
        null=True,
    )
    unit_price = models.DecimalField(
        verbose_name="Цена",
        help_text="Цена за единицу",
        max_digits=10,
        decimal_places=2,
    )
    adj_unit_sum = models.DecimalField(
        verbose_name="Корр. суммы",
        help_text="Корр. суммы",
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        abstract = True
