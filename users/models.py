from django.contrib.auth.models import AbstractUser
from django.db import models
import config.settings as settings
from school.models import Course, Lesson


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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='payments'
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name='payments'
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name='payments'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-payment_date']
