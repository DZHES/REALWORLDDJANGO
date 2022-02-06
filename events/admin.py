from django.contrib import admin

import events.models
from events import models

# Register your models here.

class FullEnrollsEventsFilter(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'full_enrolls_events_filter'

    def lookups(self, request, model_admin):
        filter_list = (
            ('0', '<= 50%'),
            ('1', '> 50%'),
            ('2', 'sold-out')
        )
        return filter_list

    def queryset(self, request, queryset):
        list_id = []
        if self.value() == '0':
            for event in queryset:
                if event.display_enroll_count() <= round(event.participants_number / 2):
                    list_id.append(event.id)
            return queryset.filter(id__in=list_id)
        elif self.value() == '1':
            for event in queryset:
                if event.display_enroll_count() > round(event.participants_number / 2) and (event.participants_number - event.display_enroll_count()) != 0:
                    list_id.append(event.id)
            return queryset.filter(id__in=list_id)
        elif self.value() == '2':
            for event in queryset:
                if event.participants_number - event.display_enroll_count() == 0:
                    list_id.append(event.id)
            return queryset.filter(id__in=list_id)
        return queryset

class ReviewsInstanceInline(admin.TabularInline):
    model = events.models.Review
    readonly_fields = ('id_review', 'user', 'event', 'rate', 'text', 'created', 'updated')
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

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
    list_filter = [FullEnrollsEventsFilter, 'category', 'features']
    readonly_fields = ['display_enroll_count', 'display_places_left', 'id']
    fields = ['id', 'title', 'description', 'date_start', 'participants_number', 'is_private', 'category', 'features', 'display_enroll_count', 'display_places_left']
    inlines = [ReviewsInstanceInline, ]
    filter_horizontal = ['features']
    list_select_related = ['category']


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
    list_select_related = ['event']

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    list_display = ['id', 'user', 'event']
    list_display_links = ['id', 'user', 'event']
    list_filter = ['created', 'event']
    fields = ['id', 'created', 'updated']
    list_select_related = ['user', 'event']
