from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.CustomSignUpView.as_view(), name='sign_up'),
]