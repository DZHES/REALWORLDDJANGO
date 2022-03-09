from django.contrib.auth.forms import UserCreationForm  #базовая форма для регистрации нового пользователя


from utils.forms import update_fields_widget # импортируем виджет

class CustomUserCreationForm(UserCreationForm): #форма для регистрации нового пользователя

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('username', 'password1', 'password2'), 'form-control')