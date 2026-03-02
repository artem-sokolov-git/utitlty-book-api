from django.utils.formats import date_format

from src.apps.readings.models.base_reading_model import BaseReadingModel
from src.apps.readings.querysets import ElectReadingQuerySet


class ElectReading(BaseReadingModel):
    objects = ElectReadingQuerySet.as_manager()

    def __str__(self):
        month = date_format(self.reading_date, "F Y")
        return f"{month} · {self.reading_value} кВт"

    class Meta:
        verbose_name = "показание электричества"
        verbose_name_plural = "показания электричества"
