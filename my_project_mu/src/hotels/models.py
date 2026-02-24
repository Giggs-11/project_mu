
# Create your models here.
from django.db import models

class Room(models.Model):
    description = models.TextField(verbose_name="Описание")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ночь")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Номер отеля"
        verbose_name_plural = "Номер отеля"
        indexes = [
            models.Index(fields=["price_per_night"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"#Room{self.pk} - {self.price_per_night}/night"
