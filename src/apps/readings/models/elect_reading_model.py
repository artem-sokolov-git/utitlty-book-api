from django.db import models
from django.utils.formats import date_format

from src.apps.readings.models.base_reading_model import BaseReadingModel
from src.apps.readings.querysets import ElectReadingQuerySet


class ElectReading(BaseReadingModel):
    objects = ElectReadingQuerySet.as_manager()

    reading_value = models.PositiveIntegerField(
        verbose_name="Показание счетчика (кВт)",
        help_text="Текущее показание на дату снятия",
    )

    reading_qty = models.PositiveIntegerField(
        verbose_name="Потребление электричества (кВт)",
        help_text="Количество потребленного электричества",
    )

    def __str__(self):
        month = date_format(self.reading_date, "F Y")
        return f"{month} · {self.reading_value} · {self.reading_qty}"

    class Meta:
        verbose_name = "показание электричества"
        verbose_name_plural = "показания электричества"
