from events import views
from django.urls import path
from django.views.decorators.http import require_POST

app_name = 'events'

urlpatterns = [
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event_update/', views.EventCreateView.as_view(), name='event_update'),
    path('enroll_event/', require_POST(views.EnrollCreationView.as_view()), name='enroll_create'),
]