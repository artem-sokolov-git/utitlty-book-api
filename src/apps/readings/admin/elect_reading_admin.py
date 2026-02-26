from django.contrib import admin
from django.utils import timezone

from src.apps.readings.models import ElectReading


@admin.register(ElectReading)
class ElectReadingAdmin(admin.ModelAdmin):
    list_display = [
        "reading_date",
        "reading_value_display",
        "reading_qty_display",
        "elect_sum_display",
        "unit_price_display",
    ]
    ordering = ["-reading_date"]

    fieldsets = (
        (
            "Электричество",
            {
                "fields": [
                    "reading_date",
                    "reading_value",
                    "reading_qty",
                    "unit_price",
                ],
            },
        ),
    )

    @admin.display(description="Показание (кВт)")
    def reading_value_display(self, obj):
        return f"{obj.reading_value} кВт"

    @admin.display(description="Потребление (кВт)")
    def reading_qty_display(self, obj):
        return f"{obj.reading_qty} кВт"

    @admin.display(description="Цена")
    def unit_price_display(self, obj):
        return f"{obj.unit_price} ₴"

    @admin.display(description="Сумма")
    def elect_sum_display(self, obj):
        return f"{obj.elect_sum} ₴"

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["reading_date"] = timezone.now().date().isoformat()
        last = ElectReading.objects.order_by("-reading_date").first()
        if last:
            initial["unit_price"] = last.unit_price
        return initial

    def get_queryset(self, request):
        return ElectReading.objects.with_costs()
