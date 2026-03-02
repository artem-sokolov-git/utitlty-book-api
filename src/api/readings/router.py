from typing import List

from ninja import Query, Router

from src.api.readings.schemas import ElectReadingFilters, ElectReadingOut, GasReadingFilters, GasReadingOut
from src.apps.readings.models import ElectReading, GasReading

router = Router(tags=["readings"])


@router.get("/electricity", response=List[ElectReadingOut])
def list_elect_readings(request, filters: ElectReadingFilters = Query(...)):
    pks = ElectReading.objects.all()
    if filters.year:
        pks = pks.filter(reading_date__year=filters.year)
    if filters.month:
        pks = pks.filter(reading_date__month=filters.month)
    qs = ElectReading.objects.with_elect_reading_sum().filter(pk__in=pks).order_by("-reading_date")
    if filters.last:
        qs = qs[:1]
    return qs


@router.get("/gas", response=List[GasReadingOut])
def list_gas_readings(request, filters: GasReadingFilters = Query(...)):
    pks = GasReading.objects.all()
    if filters.year:
        pks = pks.filter(reading_date__year=filters.year)
    if filters.month:
        pks = pks.filter(reading_date__month=filters.month)
    qs = GasReading.objects.with_declaration_values().with_trans_sum().filter(pk__in=pks).order_by("-reading_date")
    if filters.last:
        qs = qs[:1]
    return qs
