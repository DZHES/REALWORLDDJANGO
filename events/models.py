from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=90, default='', verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.title

    def display_event_count(self):
        return self.events.count()

    display_event_count.short_description = 'Количество событий'

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
    logo = models.ImageField(upload_to='events/event/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'

    def __str__(self):
        return self.title

    def display_enroll_count(self):
        return self.enrolls.count()

    display_enroll_count.short_description = 'Количество записей'

    def display_places_left(self):
        count, total = self.display_enroll_count(), self.participants_number
        if count <= round(total / 2):
            return f'{total-count} (<= 50%)'
        elif count > round(total / 2):
            if (total - count) != 0:
                return f'{total-count}(<50%)'
            else:
                return f'{0}(sold-out)'

    display_places_left.short_description = 'Осталось мест'

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.pk)])

    @property
    def rate(self):
        count_reviews = self.reviews.count()
        sum_rate = 0
        for review in self.reviews.all():
            sum_rate += review.rate
        return round(sum_rate / count_reviews, 1)

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/svg-icon/event.svg'


class Enroll(models.Model):
    user = models.ForeignKey(User, related_name='enrolls', null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='enrolls', null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')


    class Meta:
        verbose_name_plural = 'Записи на события'
        verbose_name = 'Запись на событие'

    def __str__(self):
        return f'{self.created}'

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
        return  f'{self.user} - {self.event}'

    def id_review(self):
        return f'{self.id}'

    id_review.short_description = 'id'