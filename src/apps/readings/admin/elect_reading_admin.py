from django.contrib import admin

from src.apps.readings.admin.base_reading_admin import BaseReadingAdmin
from src.apps.readings.models import ElectReading


@admin.register(ElectReading)
class ElectReadingAdmin(BaseReadingAdmin):
    last_value_fields = ["unit_price"]

    list_display = [
        "reading_date",
        "reading_value_display",
        "reading_qty_display",
        "unit_price_display",
        "total_elect_reading_sum_display",
        "adj_unit_sum_display",
    ]

    fieldsets = (
        (
            "Электроэнергия",
            {
                "fields": [
                    "reading_date",
                    "reading_value",
                    "unit_price",
                ],
            },
        ),
        (
            "Корректировка",
            {
                "fields": [
                    "reading_qty",
                    "adj_unit_sum",
                ],
                "classes": ["collapse"],
            },
        ),
    )

    @admin.display(description="Показание")
    def reading_value_display(self, obj):
        return f"{obj.reading_value} кВт"

    @admin.display(description="Потребление")
    def reading_qty_display(self, obj):
        qty = obj.reading_qty if obj.reading_qty is not None else obj.elect_reading_qty
        return f"{qty} кВт" if qty is not None else "—"

    @admin.display(description="Цена")
    def unit_price_display(self, obj):
        return f"{obj.unit_price} ₴"

    @admin.display(description="Сумма")
    def total_elect_reading_sum_display(self, obj):
        return f"{obj.total_elect_reading_sum} ₴"

    @admin.display(description="Корр. суммы")
    def adj_unit_sum_display(self, obj):
        return self._colored_value_display(obj.adj_unit_sum, "₴")

    def get_queryset(self, request):
        return ElectReading.objects.with_elect_reading_sum()
