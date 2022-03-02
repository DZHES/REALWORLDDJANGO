from events import views
from django.urls import path
from django.views.decorators.http import require_POST

app_name = 'events'

urlpatterns = [
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event_create/', views.EventCreateView.as_view(), name='event_create'),
    path('event_enroll/', require_POST(views.EnrollCreationView.as_view()), name='event_enroll'),
    path('event_update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('event_delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
]