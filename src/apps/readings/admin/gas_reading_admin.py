from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from src.apps.readings.models import GasReading


@admin.register(GasReading)
class GasReadingAdmin(admin.ModelAdmin):
    list_display = [
        "reading_date",
        "reading_value_display",
        "gas_dec_reading_display",
        "reading_qty_display",
        "gas_dec_diff_display",
        "gas_dec_sum_display",
        "unit_price_display",
        "trans_cost_display",
    ]
    ordering = ["-reading_date"]

    fieldsets = (
        (
            "Газ",
            {
                "fields": (
                    [
                        "reading_date",
                        "reading_value",
                        "reading_qty",
                        "unit_price",
                        "trans_cost",
                    ]
                ),
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
        diff = obj.gas_dec_diff
        color = "Crimson" if diff > 0 else "MediumSeaGreen" if diff == 0 else "CadetBlue"
        sign = "+" if diff > 0 else ""
        return format_html('<span style="color: {}; font-weight: 600">{}{} м³</span>', color, sign, diff)

    @admin.display(description="Сумма (Д)")
    def gas_dec_sum_display(self, obj):
        return f"{obj.gas_dec_sum} ₴"

    @admin.display(description="Цена (Д)")
    def unit_price_display(self, obj):
        return f"{obj.unit_price} ₴"

    @admin.display(description="Транспортировка")
    def trans_cost_display(self, obj):
        return f"{obj.trans_cost} ₴"

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["reading_date"] = timezone.now().date().isoformat()
        last = GasReading.objects.order_by("-reading_date").first()
        if last:
            initial["unit_price"] = last.unit_price
            initial["trans_cost"] = last.trans_cost
        return initial

    def get_queryset(self, request):
        return GasReading.declared.with_readings().with_diff().with_costs()
