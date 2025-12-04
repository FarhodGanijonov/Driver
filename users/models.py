from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, full_name, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        if not full_name:
            raise ValueError('The Full Name field must be set')

        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, full_name, password, **extra_fields)

# Client va Driver userlar uchun model
class AbstractUser(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [('Male', 'Erkak'), ('Female', 'Ayol')]
    ROLE_CHOICES = [('client', 'client'), ('driver', 'driver')]
    STATUS_CHOICES = [
        ('online', 'Onlayn'), ('offline', 'Offline'), ('busy', 'Band'),
        ('active', 'Faol'), ('inactive', 'Faol emas'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    avatar = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_driver_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    point = gis_models.PointField(srid=4326, default=Point(69.279759, 41.311081), blank=True, null=True)

    current_order = models.ForeignKey(
        'order.Order',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_driver' )

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['full_name']

    def save(self, *args, **kwargs):
        if self.role == 'driver' and self.status not in ['offline', 'online', 'busy']:
            raise ValueError("Driver status must be 'online', 'offline', or 'busy'")
        if self.role == 'client' and self.status not in ['active', 'inactive']:
            raise ValueError("Client status must be 'active' or 'inactive'")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} | {self.phone}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['created_at']
        unique_together = ('phone', 'role')

