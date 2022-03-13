from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, PasswordChangeForm,
                                            SetPasswordForm, PasswordResetForm)
from allauth.account.forms import LoginForm
from accounts.models import Profile
from django import forms
from utils.forms import update_fields_widget # импортируем виджет

class CustomUserCreationForm(UserCreationForm): #форма для регистрации нового пользователя

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('username', 'password1', 'password2'), 'form-control')

# class CustomAuthenticationForm(AuthenticationForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         update_fields_widget(self, ('username', 'password'), 'form-control')
class CustomAuthenticationForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('login', 'password'), 'form-control')

class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('old_password', 'new_password1', 'new_password2'), 'form-control')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', )

class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('email',), 'form-control')

class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('new_password1', 'new_password2',), 'form-control')