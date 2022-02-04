from django.contrib import admin
from events import models

# Register your models here.

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'date_start',
                    'is_private',
                    'category',
                    'participants_number',
                    'display_enroll_count',
                    'display_places_left'
                    ]
    ordering = ['date_start']
    search_fields = ['title']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_event_count']
    list_display_links = ['id', 'title']

@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']

@admin.register(models.Enroll)
class EnrollAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ['id', 'user', 'event']
    list_display_links = ['id', 'user', 'event']

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated',)
    list_display = ['id', 'user', 'event']
    list_display_links = ['id', 'user', 'event']
    list_filter = ['created', 'updated']
