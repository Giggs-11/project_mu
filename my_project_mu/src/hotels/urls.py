from django.urls import path
from hotels.views import RoomCreateView, RoomDeleteView, RoomListView

urlpatterns = [
    path("create/", RoomCreateView.as_view(), name="room-create"),
    path("list/", RoomListView.as_view(), name="room-list"),
    path("<int:room_id>/delete/", RoomDeleteView.as_view(), name="room-delete"),
]