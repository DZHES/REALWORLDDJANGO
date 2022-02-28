import datetime
from django.shortcuts import render, get_object_or_404
from events.models import Event, Review, Enroll
#импортируем HttpResponseForbidden для вывода ошибки
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_POST
#импортируем базовый класс ListView для представления списка событий
#импортируем базовый класс DetailView для представления детальной страницы события
#импортируем базовый класс CreateView для создания нового объекта
#импортируем базовый класс UpdateView для редактирования объекта
from django.views.generic import ListView, DetailView, CreateView
#импортируем форму для создания объекта
from events.forms import EventCreationForm, EnrollCreationForm
#импортируем reverse_lazy для переопределения переадресации
from django.urls import reverse_lazy
#импортируеи messages для вывода сообщений
from django.contrib import messages

class EventListView(ListView):
    model = Event  #Передаем модель Event
    template_name = 'events/event_list.html' #задаём шаблон в атрибуте template_name
    paginate_by = 9    #Добавляем пагинацию для вывода 9 событий на странице

    def get_queryset(self):      #добавляем сортировку списка объектов по убыванию
        queryset = super().get_queryset()
        return queryset.order_by("-pk")

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['display_places_left'] = self.object.display_places_left()[0]
        context['enroll_add'] = EnrollCreationForm(initial={'user' : self.request.user, 'event' : self.object,
                                                             'created' : datetime.date.today().strftime('%d.%m.%Y')})
        return context

class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventCreationForm #создаем модель формы EventCreationForm
    success_url = reverse_lazy("events:event_list") #при успешном создании объекта будет переадресация на список событий

    def get(self, request, *args, **kwargs):  #создание события будет доступно только для залогиненных пользователей
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form): #вывод сообщения если валидация прошла успешно
        messages.success(self.request, 'Новое событие создано успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors()) #вывод сообщения если валидация прошла неудачно
        return super().form_valid(form)

class EnrollCreationView(CreateView):
    model = Enroll
    form_class = EventCreationForm

    def form_valid(self, form):
        messages.success(self.request, 'Вы записаны на событие')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.event.get_absolute_url()



# class EnrollAddToEventView(CreateView):
#     model = Enroll
#     form_class = EnrollAddToEventForm
#
#     def post(self, request, *args, **kwargs):  #запись на  событие будет доступно только для залогиненных пользователей
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden('Недостаточно прав')
#         return super().get(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return self.object.event.get_absolute_url()
#
#     def form_valid(self, form):
#         messages.success(self.request, 'Вы записаны на событие')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, form.non_field_errors())
#         event = form.cleaned_data.get('event', None)
#         if not event:
#             event = get_object_or_404(Event, pk=form.data.get('event'))
#         redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
#         return HttpResponseRedirect(redirect_url)

@require_POST
def create_review(request):
    event_id = request.POST.get('event_id', '')
    rate = int(request.POST.get('rate', 0) or 0)
    text = request.POST.get('text', '')


    data = {
        'ok' : True,
        'msg' : '',
        'rate' : int(rate),
        'text' : text,
        'created': datetime.date.today().strftime('%d.%m.%Y'),
        'user_name': request.user.__str__(),
    }
    if event_id == '' or event_id == '0':
        data['ok'] = False
        data['msg'] = 'Такого события нет'
        return JsonResponse(data)

    new_event = Event.objects.get(pk=int(event_id))

    if not request.user.is_authenticated:
        data['msg'] = 'Отзывы могут оставлять только зарегистрированные пользователи'
        data['ok'] = False
        return JsonResponse(data)

    if Review.objects.filter(user=request.user, event=new_event).exists():
        data['msg'] = 'Вы уже отправляли отзыв к этому событию'
        data['ok'] = False
        return JsonResponse(data)

    if data['rate'] == '' or data['text'] == '':
        data['msg'] = 'Оценка и текст отзыва - обязательные поля'
        data['ok'] = False
        return JsonResponse(data)

    new_review = Review(
        user = request.user,
        event = new_event,
        rate = data['rate'],
        text = data['text'],
        created = data['created'],
        updated = data['created'],
    )

    new_review.save()

    return JsonResponse(data)







