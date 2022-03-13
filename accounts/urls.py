from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from .forms import CustomPasswordChangeForm

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.CustomSignUpView.as_view(), name='sign_up'),
    path('sign-in/', views.CustomLoginView.as_view(), name='sign_in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/',
         PasswordChangeView.as_view(
             template_name='accounts/registration/password_change.html',
             form_class=CustomPasswordChangeForm,
             success_url=reverse_lazy('accounts:password_change_done')
         ),
         name='password_change'),
    path('password-change-done/',
         PasswordChangeDoneView.as_view(
             template_name='accounts/registration/password_change_done.html'
         ),
         name='password_change_done'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile')
]