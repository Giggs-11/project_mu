from datetime import date
from decimal import Decimal

from django.test import TestCase

from bookings.models import Booking
from bookings.service import create_booking, delete_booking, list_bookings
from hotels.models import Room
from hotels.service import create_room


class BookingTest(TestCase):
    def setUp(self):
        self.room = create_room(description='Люкс', price_per_night=Decimal('5000'))

    def test_create_booking(self):
        booking = create_booking(
            room_id=self.room.pk,
            date_start=date(2024, 6, 20),
            date_end=date(2024, 6, 25),
        )
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.date_start, date(2024, 6, 20)),
        self.assertEqual(booking.date_end, date(2024, 6, 25))

    def test_raises_if_room_not_found(self):
        with self.assertRaises(Room.DoesNotExist):
            create_booking(
                room_id=99999,
                date_start=date(2024, 6, 20),
                date_end=date(2024, 6, 25),
        )

    def test_raises_if_date_start_after_date_end(self):
        with self.assertRaises(ValueError):
            create_booking(
                room_id=self.room.pk,
                date_start=date(2024, 6, 25),
                date_end=date(2024, 6, 20),
            )

    def test_overlap_same_dates(self):
        create_booking(
            room_id=self.room.pk,
            date_start=date(2024, 6, 20),
            date_end=date(2024, 6, 25),
        )
        with self.assertRaises(ValueError):
            create_booking(
                room_id=self.room.pk,
                date_start=date(2024, 6, 20),
                date_end=date(2024, 6, 25),
            )


class DeleteBookingTest(TestCase):
    def setUp(self):
        self.room = create_room(description='Люкс', price_per_night=Decimal('5000'))
        self.booking = create_booking(
            room_id=self.room.pk,
            date_start=date(2024, 6, 20),
            date_end=date(2024, 6, 25),
        )

    def test_delete_booking(self):
        delete_booking(self.booking.pk)
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_raises_if_room_not_found(self):
        with self.assertRaises(Booking.DoesNotExist):
            delete_booking(99999)


class ListBookingsTest(TestCase):
    def setUp(self):
        self.room = create_room(description="Люкс", price_per_night=Decimal("5000"))
        create_booking(self.room.pk, date(2024, 6, 20), date(2024, 6, 25))
        create_booking(self.room.pk, date(2024, 7, 1), date(2024, 7, 5))
        create_booking(self.room.pk, date(2024, 5, 10), date(2024, 5, 15))


    def test_returns_bookings_for_room(self):
        bookings = list_bookings(self.room.pk)
        self.assertEqual(len(bookings), 3)

    def test_sorted_by_date_start(self):
        bookings = list_bookings(self.room.pk)
        dates = [b.date_start for b in bookings]
        self.assertEqual(dates, sorted(dates))

