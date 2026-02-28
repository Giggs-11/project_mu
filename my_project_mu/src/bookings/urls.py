from django.urls import path

from bookings.views import BookingCreateView, BookingDeleteView, BookingListView

urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("list/", BookingListView.as_view(), name="booking-list"),
    path("<int:booking_id>/delete/", BookingDeleteView.as_view(), name="booking-delete"),
]