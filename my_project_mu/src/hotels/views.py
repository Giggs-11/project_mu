from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.views import View

from hotels.models import Room
from hotels.service import create_room, delete_room, list_rooms


class RoomCreateView(View):
    def post(self, request):
        description = request.POST.get("description", "").strip()
        price_raw = request.POST.get("price_per_night")

        if not description:
            return JsonResponse({"error": "требуется описание"}, status=400)
        if not price_raw:
            return JsonResponse({"error": "требуется цена за ночь"}, status=400)

        try:
            price = Decimal(price_raw)
        except InvalidOperation:
            return JsonResponse({"error": "цена за ночь должна быть указана в виде числа"}, status=400)

        if price <= 0:
            return JsonResponse({"error": "цена за ночь должна быть положительной"}, status=400)

        room = create_room(description=description, price_per_night=price)
        return JsonResponse({"room_id": room.pk}, status=201)


class RoomDeleteView(View):
    def delete(self, request, room_id):
        try:
            delete_room(room_id)
        except Room.DoesNotExist as e:
            return JsonResponse({"error": str(e)}, status=404)

        return JsonResponse({"deleted": True})


class RoomListView(View):
    VALID_SORT_VALUES = {"price_asc", "price_desc", "date_asc", "date_desc"}

    def get(self, request):
        sort = request.GET.get("sort", "date_asc")
        if sort not in self.VALID_SORT_VALUES:
            return JsonResponse(
                {"error": f"сортировка должна быть одной из: {', '.join(self.VALID_SORT_VALUES)}"},
                status=400,
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