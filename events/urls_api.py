from events import views
from django.urls import path

app_name = 'api_events'

urlpatterns = [
    path('reviews/create/', views.create_review, name='create_review')
]
