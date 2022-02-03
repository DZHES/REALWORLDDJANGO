from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=90, default='', verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=100, default='', verbose_name='Свойство события')

    class Meta:
            verbose_name_plural = 'Свойства событий'
            verbose_name = 'Свойство события'

class Event(models.Model):
    title = models.CharField(max_length=200, default='', verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(verbose_name='Количество участников')
    is_private = models.BooleanField(default=False, verbose_name='Частное')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='events')
    features = models.ManyToManyField(Feature)

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'

    def __str__(self):
        return self.title

class Enroll(models.Model):
    user = models.ForeignKey(User, related_name='enrolls', null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='events', null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)