from events.models import Event, Enroll, Category, Feature
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

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if Event.objects.filter(title=title).exists():
            raise forms.ValidationError(f'Событие с таким названием уже имеется')
        return cleaned_data

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
        return cleaned_data

class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class EventFilterForm(forms.Form):
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), required=False)
    features = forms.ModelMultipleChoiceField(label='Свойства', queryset=Feature.objects.all(), required=False)
    date_start = forms.DateTimeField(label='Дата начала',
                                     widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
                                     required=False)
    date_end = forms.DateTimeField(label='Дата конца',
                                   widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
                                   required=False)
    is_private = forms.BooleanField(label='Приватное',
                                    widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                                    required=False)
    is_available = forms.BooleanField(label='Есть места',
                                      widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                                      required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['features'].widget.attrs.update({'class': 'form-select', 'multiple': True})
        self.fields['date_start'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_end'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})