from django.db import models


class Booking(models.Model):
    room = models.ForeignKey(
        'hotels.Room',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Номер отеля'
    )
    date_start = models.DateField(verbose_name="Дата начала")
    date_end = models.DateField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        indexes = [
            models.Index(fields=['room', 'date_start']),
            models.Index(fields=['date_start', 'date_end']),
        ]

    def __str__(self):
        return f"Bookings{self.pk} | Room{self.room_id} | {self.date_start} - {self.date_end}"

