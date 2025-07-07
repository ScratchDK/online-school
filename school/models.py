from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание")
    preview_image = models.ImageField(
        upload_to="images/course/", blank=True, null=True, verbose_name="Изображение"
    )
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
        verbose_name="Владелец",
    )
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Цена"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание")
    preview_image = models.ImageField(
        upload_to="images/lesson/", blank=True, null=True, verbose_name="Изображение"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lessons",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Subscription(models.Model):
    course = models.ForeignKey(
        "school.Course",
        on_delete=models.CASCADE,
        related_name="subscription",
        verbose_name="Курс",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="subscription",
        verbose_name="Пользователь",
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата подписки"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]
