from django.contrib import admin

from src.apps.readings.admin.base_reading_admin import BaseReadingAdmin
from src.apps.readings.models import GasReading


@admin.register(GasReading)
class GasReadingAdmin(BaseReadingAdmin):
    last_value_fields = ["unit_price", "trans_sum"]

    list_display = [
        "reading_date",
        "reading_value_display",
        "dec_reading_value_display",
        "reading_qty_display",
        "dec_real_reading_diff_display",
        "unit_price_display",
        "total_dec_reading_sum_display",
        "adj_unit_sum_display",
        "trans_sum_display",
        "adj_trans_sum_display",
    ]

    fieldsets = (
        (
            "Газ",
            {
                "fields": [
                    "reading_date",
                    "reading_value",
                    "reading_qty",
                    "unit_price",
                    "trans_sum",
                ],
            },
        ),
        (
            "Корректировка",
            {
                "fields": [
                    "adj_trans_sum",
                    "adj_unit_sum",
                ],
                "classes": ["collapse"],
            },
        ),
    )

    @admin.display(description="Показание (Р)")
    def reading_value_display(self, obj):
        return f"{obj.reading_value} м³"

    @admin.display(description="Показание (Д)")
    def dec_reading_value_display(self, obj):
        return f"{obj.dec_reading_value} м³"

    @admin.display(description="Потребление (Д)")
    def reading_qty_display(self, obj):
        return f"{obj.reading_qty} м³"

    @admin.display(description="Долг/профицит (Р/Д)")
    def dec_real_reading_diff_display(self, obj):
        return self._colored_value_display(obj.dec_real_reading_diff, "м³")

    @admin.display(description="Цена (Д)")
    def unit_price_display(self, obj):
        return f"{obj.unit_price} ₴"

    @admin.display(description="Сумма (Д)")
    def total_dec_reading_sum_display(self, obj):
        return f"{obj.total_dec_reading_sum} ₴"

    @admin.display(description="Корр. суммы (Д)")
    def adj_unit_sum_display(self, obj):
        return self._colored_value_display(obj.adj_unit_sum, "₴")

    @admin.display(description="Транспортировка")
    def trans_sum_display(self, obj):
        return f"{obj.total_trans_sum} ₴"

    @admin.display(description="Корр. транспортировки")
    def adj_trans_sum_display(self, obj):
        return self._colored_value_display(obj.adj_trans_sum, "₴")

    def get_queryset(self, request):
        return GasReading.objects.with_declaration_values().with_trans_sum()
