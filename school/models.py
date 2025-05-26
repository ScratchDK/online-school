from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(upload_to='images/course/', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(upload_to='images/lesson/', blank=True, null=True, verbose_name='Изображение')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['title']

    def __str__(self):
        return self.title
