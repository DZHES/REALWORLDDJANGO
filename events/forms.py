from events.models import Event, Enroll
from django import forms

class EventCreationForm(forms.ModelForm):  #Создаём модельную форму
    date_start = forms.DateTimeField(label='Дата начала',
                                        widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                                   attrs={'type' : 'datetime-local'})
                                     )
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_start'].widget.attrs.update({'class' : 'form-control'})

class EnrollCreationForm(forms.ModelForm):
    class Meta:
        model = Enroll
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        event = cleaned_data.get('event')

        if Enroll.objects.filter(user=user, event=event).exists():
            raise forms.ValidationError(f'Вы уже записаны на это событие')

class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'