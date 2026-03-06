from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.exceptions import handle_exceptions
from hotels.service import create_room, delete_room, list_rooms


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(handle_exceptions, name="dispatch")
class RoomCreateView(View):
    def post(self, request):
        description = request.POST.get("description", "").strip()
        price_raw = request.POST.get("price_per_night")

        if not description:
            raise ValueError("Требуется описание")
        if not price_raw:
            raise ValueError("Требуется цена за ночь")

        try:
            price = Decimal(price_raw)
        except InvalidOperation:
            raise ValueError("Цена за ночь должно быть числом")

        if price <= 0:
            raise ValueError("Цена за ночь должен быть позитивным")

        room = create_room(description=description, price_per_night=price)
        return JsonResponse({"room_id": room.pk}, status=201)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(handle_exceptions, name="dispatch")
class RoomDeleteView(View):
    def delete(self, request, room_id):
        delete_room(room_id)
        return JsonResponse({"deleted": True})

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(handle_exceptions, name="dispatch")
class RoomListView(View):
    VALID_SORT_VALUES = {"price_asc", "price_desc", "date_asc", "date_desc"}

    def get(self, request):
        sort = request.GET.get("sort", "date_asc")
        if sort not in self.VALID_SORT_VALUES:
            raise ValueError(
                f"сортировка должна быть одной из: {', '.join(self.VALID_SORT_VALUES)}"
            )

        rooms = list_rooms(sort=sort)
        data = [
            {
                "room_id": room.pk,
                "description": room.description,
                "price_per_night": str(room.price_per_night),
                "created_at": room.created_at.isoformat(),
            }
            for room in rooms
        ]
        return JsonResponse(data, safe=False)