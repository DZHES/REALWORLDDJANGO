from events import views
from django.urls import path

app_name = 'events'

urlpatterns = [
    path('list/', views.events_list, name='event_list'),
    path('detail/<int:pk>/', views.event_detail, name='event_detail')
]