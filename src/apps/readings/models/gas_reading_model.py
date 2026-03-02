from django.db import models
from django.utils.formats import date_format

from src.apps.readings.models.base_reading_model import BaseReadingModel
from src.apps.readings.querysets import GasReadingQuerySet


class GasReading(BaseReadingModel):
    objects = GasReadingQuerySet.as_manager()

    trans_sum = models.DecimalField(
        verbose_name="Транспортировка",
        help_text="Сумма за транспортировку (по умолчанию предыдущее значение)",
        max_digits=10,
        decimal_places=2,
    )
    adj_trans_sum = models.DecimalField(
        verbose_name="Корректировка транспортировки (UAH)",
        help_text="Сумма корректировки транспортировки (положительная — доплата, отрицательная — переплата)",
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        month = date_format(self.reading_date, "F Y")
        return f"{month} · {self.reading_value} · {self.reading_qty}"

    class Meta:
        verbose_name = "показание газа"
        verbose_name_plural = "показания газа"
