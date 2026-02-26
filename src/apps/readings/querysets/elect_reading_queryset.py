from src.apps.readings.querysets.base_reading_queryset import BaseReadingQuerySet


class ElectReadingQuerySet(BaseReadingQuerySet):
    costs_field = "elect_sum"
