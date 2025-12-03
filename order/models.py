from django.db import models
from django.contrib.gis.db import models as gis_models
from users.models import AbstractUser

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('ASSIGNED', 'Assigned'),
        ('COMPLETED', 'Completed'),
    ]

    client = models.ForeignKey(
        AbstractUser,
        on_delete=models.CASCADE,
        related_name='client_orders'
    )
    driver = models.ForeignKey(
        AbstractUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='driver_orders'
    )

    description = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='CREATED'
    )

    client_is_finished = models.BooleanField(default=False)
    location = gis_models.PointField(
        srid=4326,
        blank=True,
        null=True,
        default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.client.full_name}"
