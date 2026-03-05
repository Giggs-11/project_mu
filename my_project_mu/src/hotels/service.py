from hotels.models import Room

# Словарь маппинга
VALID_SORT_FIELDS = {
    "price_asc": "price_per_night",
    "price_desc": "-price_per_night",
    "date_asc": "created_at",
    "date_desc": "-created_at",
}

def create_room(description: str, price_per_night) -> Room:
    return Room.objects.create(
        description=description,
        price_per_night=price_per_night,
    )


def delete_room(room_id: int) -> None:
    deleted_count, _ = Room.objects.filter(pk=room_id).delete()
    if not deleted_count:
        raise Room.DoesNotExist(f'Комната {room_id} не найдена')


def list_rooms(sort: str = 'date_asc')-> list[Room]:
    # .get(sort,"created_at") защищает от ошибок и потенциальных манипуляций с запросами.
    order_field = VALID_SORT_FIELDS.get(sort, 'created_at')
    # заставляет ORM выполнить SQL-запрос немедленно и вернуть реальный список объектов.
    return list(Room.objects.order_by(order_field))
