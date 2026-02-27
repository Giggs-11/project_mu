from datetime import datetime

from django.http import JsonResponse
from django.views import View

from bookings.models import Booking
from bookings.service import create_booking, delete_booking, list_bookings
from hotels.models import Room


DATE_FORMAT = "%Y-%m-%d"

# функция валидации + парсинга даты
def parse_date(value: str | None, field_name: str):
    if not value:
        return None, f"требуется {field_name}"
    try:
        return datetime.strptime(value, DATE_FORMAT).date(), None
    except ValueError:
        return None, f"{field_name} должно быть в формате YYYY-MM-DD"


class BookingCreateView(View):
    def post(self, request):
        room_id_raw = request.POST.get("room_id")
        if not room_id_raw:
            return JsonResponse({"error": "требуется указать room_id"}, status=400)

        try:
            room_id = int(room_id_raw)
        except ValueError:
            return JsonResponse({"error": "room_id должен быть числом"}, status=400)

        date_start, err = parse_date(request.POST.get("date_start"), "date_start")
        if err:
            return JsonResponse({"error": err}, status=400)

        date_end, err = parse_date(request.POST.get("date_end"), "date_end")
        if err:
            return JsonResponse({"error": err}, status=400)

        try:
            booking = create_booking(room_id=room_id, date_start=date_start, date_end=date_end)
        except Room.DoesNotExist as e:
            return JsonResponse({"error": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({"booking_id": booking.pk}, status=201)


class BookingDeleteView(View):
    def delete(self, request, booking_id):
        try:
            delete_booking(booking_id)
        except Booking.DoesNotExist as e:
            return JsonResponse({"error": str(e)}, status=404)

        return JsonResponse({"deleted": True})


class BookingListView(View):
    def get(self, request):
        room_id_raw = request.GET.get("room_id")
        if not room_id_raw:
            return JsonResponse({"error": "требуется указать room_id"}, status=400)

        try:
            room_id = int(room_id_raw)
        except ValueError:
            return JsonResponse({"error": "room_id должен быть числом"}, status=400)

        try:
            bookings = list_bookings(room_id=room_id)
        except Room.DoesNotExist as e:
            return JsonResponse({"error": str(e)}, status=404)

        data = [
            {
                "booking_id": b.pk,
                "date_start": b.date_start.isoformat(),
                "date_end": b.date_end.isoformat(),
            }
            for b in bookings
        ]
        return JsonResponse(data, safe=False)