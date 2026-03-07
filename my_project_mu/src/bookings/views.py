from datetime import date, datetime
from typing import Optional, Tuple

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bookings.service import create_booking, delete_booking, list_bookings
from core.exceptions import handle_exceptions

DATE_FORMAT = "%Y-%m-%d"


def parse_date(
    value: Optional[str], field_name: str
) -> Tuple[Optional[date], Optional[str]]:
    if not value:
        return None, f"Требуется {field_name} "
    try:
        return datetime.strptime(value, DATE_FORMAT).date(), None
    except ValueError:
        return None, f"{field_name} должно быть в формате YYYY-MM-DD"

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(handle_exceptions, name="dispatch")
class BookingCreateView(View):
    def post(self, request):
        room_id_raw = request.POST.get("room_id")
        if not room_id_raw:
            raise ValueError("Требуется номер комнаты")

        try:
            room_id = int(room_id_raw)
        except ValueError:
            raise ValueError("Номер комнаты должно быть целым числом")

        date_start, err = parse_date(request.POST.get("date_start"), "date_start")
        if err:
            raise ValueError(err)

        date_end, err = parse_date(request.POST.get("date_end"), "date_end")
        if err:
            raise ValueError(err)

        booking = create_booking(
            room_id=room_id,
            date_start=date_start,
            date_end=date_end,
        )
        return JsonResponse({"booking_id": booking.pk}, status=201)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(handle_exceptions, name="dispatch")
class BookingDeleteView(View):
    def delete(self, request, booking_id):
        delete_booking(booking_id)
        return JsonResponse({"deleted": True})

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(handle_exceptions, name="dispatch")
class BookingListView(View):
    def get(self, request):
        room_id_raw = request.GET.get("room_id")
        if not room_id_raw:
            raise ValueError("Требуется номер комнаты")

        try:
            room_id = int(room_id_raw)
        except ValueError:
            raise ValueError("Номер комнаты должно быть целым числом")

        bookings = list_bookings(room_id=room_id)
        data = [
            {
                "booking_id": b.pk,
                "date_start": b.date_start.isoformat(),
                "date_end": b.date_end.isoformat(),
            }
            for b in bookings
        ]
        return JsonResponse(data, safe=False)