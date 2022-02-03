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

    def __str__(self):
        return self.title

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
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')


    class Meta:
        verbose_name_plural = 'Записи на события'
        verbose_name = 'Запись на событие'

    def __str__(self):
        return self.user

class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='reviews', null=True, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(null=True, verbose_name='Оценка пользователя')
    text = models.TextField(default='', verbose_name='Текст пользователя')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Отзывы на события'
        verbose_name = 'Отзыв на событие'

    def __str__(self):
        return  self.user