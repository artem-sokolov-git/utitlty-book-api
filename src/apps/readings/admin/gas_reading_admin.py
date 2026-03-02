from django.contrib import admin

from src.apps.readings.admin.base_reading_admin import BaseReadingAdmin
from src.apps.readings.models import GasReading


@admin.register(GasReading)
class GasReadingAdmin(BaseReadingAdmin):
    last_value_fields = ["unit_price", "trans_cost"]

    list_display = [
        "reading_date",
        "reading_value_display",
        "gas_dec_reading_display",
        "reading_qty_display",
        "gas_dec_diff_display",
        "unit_price_display",
        "gas_dec_sum_display",
        "adj_costs_display",
        "trans_cost_display",
        "adj_trans_cost_display",
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
                    "trans_cost",
                ],
            },
        ),
        (
            "Корректировка",
            {
                "fields": [
                    "adj_trans_cost",
                    "adj_costs",
                ],
                "classes": ["collapse"],
            },
        ),
    )

    @admin.display(description="Показание (Р)")
    def reading_value_display(self, obj):
        return f"{obj.reading_value} м³"

    @admin.display(description="Показание (Д)")
    def gas_dec_reading_display(self, obj):
        return f"{obj.gas_dec_reading} м³"

    @admin.display(description="Потребление (Д)")
    def reading_qty_display(self, obj):
        return f"{obj.reading_qty} м³"

    @admin.display(description="Долг/профицит")
    def gas_dec_diff_display(self, obj):
        return self._colored_value_display(obj.gas_dec_diff, "м³")

    @admin.display(description="Цена (Д)")
    def unit_price_display(self, obj):
        return f"{obj.unit_price} ₴"

    @admin.display(description="Сумма (Д)")
    def gas_dec_sum_display(self, obj):
        return f"{obj.gas_dec_sum} ₴"

    @admin.display(description="Корр. суммы")
    def adj_costs_display(self, obj):
        return self._colored_value_display(obj.adj_costs, "₴")

    @admin.display(description="Транспортировка")
    def trans_cost_display(self, obj):
        return f"{obj.total_trans_cost} ₴"

    @admin.display(description="Корр. транспортировки")
    def adj_trans_cost_display(self, obj):
        return self._colored_value_display(obj.adj_trans_cost, "₴")

    def get_queryset(self, request):
        return GasReading.objects.with_dec_reading().with_dec_diff().with_dec_sum().with_trans_cost()
