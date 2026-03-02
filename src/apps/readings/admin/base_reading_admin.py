from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html


class BaseReadingAdmin(admin.ModelAdmin):
    last_value_fields: list[str] = []
    ordering = ["-reading_date"]

    def _colored_value_display(self, value, unit):
        if not value:
            return "—"
        color = "Crimson" if value > 0 else "CadetBlue"
        sign = "+" if value > 0 else ""
        return format_html('<span style="color: {}; font-weight: 600">{}{} {}</span>', color, sign, value, unit)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["reading_date"] = timezone.now().date().isoformat()
        if self.last_value_fields:
            last = self.model.objects.order_by("-reading_date").first()
            if last:
                for field in self.last_value_fields:
                    initial[field] = getattr(last, field)
        return initial
