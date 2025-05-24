from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CITIES_CHOICES = [
        ("Pyatigorsk", "Пятигорск"),
        ('Moscow', 'Москва'),
        ('Saint Petersburg', 'Санкт-Петербург'),
        ('Omsk', 'Омск'),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/images/', blank=True, null=True)
    cities = models.CharField(max_length=255, choices=CITIES_CHOICES, null=True, blank=True, verbose_name="Города")
    # Токен для потверждения почты при регестрации и для восстановления пароля
    confirmation_token = models.CharField(max_length=32, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
