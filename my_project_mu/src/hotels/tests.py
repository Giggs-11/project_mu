from decimal import Decimal

from django.test import TestCase

from hotels.models import Room
from hotels.service import create_room, delete_room, list_rooms


class CreateRoomTest(TestCase):
    def test_creates_room_with_correct_fields(self):
        room = create_room(description="Люкс", price_per_night=Decimal("5000"))
        self.assertEqual(room.description, "Люкс")
        self.assertEqual(room.price_per_night, Decimal("5000"))
        self.assertIsNotNone(room.pk)

    def test_room_saved_to_db(self):
        room = create_room(description="Стандарт", price_per_night=Decimal("2000"))
        self.assertTrue(Room.objects.filter(pk=room.pk).exists())


class DeleteRoomTest(TestCase):
    def setUp(self):
        self.room = create_room(description="Люкс", price_per_night=Decimal("5000"))

    def test_deletes_existing_room(self):
        delete_room(self.room.pk)
        self.assertFalse(Room.objects.filter(pk=self.room.pk).exists())

    def test_raises_if_room_not_found(self):
        with self.assertRaises(Room.DoesNotExist):
            delete_room(99999)


class ListRoomsTest(TestCase):
    def setUp(self):
        create_room(description="Эконом", price_per_night=Decimal("1000"))
        create_room(description="Стандарт", price_per_night=Decimal("3000"))
        create_room(description="Люкс", price_per_night=Decimal("5000"))

    def test_sort_price_asc(self):
        rooms = list_rooms(sort="price_asc")
        prices = [r.price_per_night for r in rooms]
        self.assertEqual(prices, sorted(prices))

    def test_sort_date_desc(self):
        rooms = list_rooms(sort="date_desc")
        dates = [r.created_at for r in rooms]
        self.assertEqual(dates, sorted(dates, reverse=True))
