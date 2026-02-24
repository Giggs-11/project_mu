from datetime import date
from django.db import transaction

from bookings.models import Booking
from hotels.models import Room

def create_booking(room_id: int, date_start: date, date_end: date) -> Booking:
    # нельзя выехать раньше, чем заехал
    if date_start >= date_end:
        raise ValueError('Дата начала должна быть меньше даты окончания')

    # если ошибка, то rollback
    with transaction.atomic():
        # блокирует выбранную строку в базе данных
        room = Room.objects.filter(pk=room_id).select_for_update().first()
        if room is None:
            raise Room.DoesNotExist(f'Комната {room_id} не найдена')
    return Booking.objects.create(
        room=room,
        date_start=date_start,
        date_end=date_end,
    )


def delete_booking(booking_id: int) -> None:
    delete_count, _ = Booking.objects.filter(pk=booking_id).delete()
    if not delete_count:
        raise Booking.DoesNotExist(f'Бронирование {booking_id} не найдено')


def list_bookings(room_id: int) -> list[Booking]:
    if not Room.objects.filter(pk=room_id).exists():
        raise Room.DoesNotExist(f'Комната {room_id} не найдена')
    # список броней будет идти в хронологическом порядке
    return list(Booking.objects.filter(room_id=room_id).order_by('date_start'))
