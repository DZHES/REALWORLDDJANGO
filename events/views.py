import datetime
from django.shortcuts import render, get_object_or_404
from events.models import Event, Review, Enroll
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from events.forms import EventCreationForm, EnrollCreationForm, EventUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages

class LoginRequiredMixin:
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
                return HttpResponseForbidden('Недостаточно прав')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав')
        return super().get(request, *args, **kwargs)

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-pk")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'События'
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['display_places_left'] = self.object.places_left()
        context['enroll_add'] = EnrollCreationForm(initial={'user' : self.request.user, 'event' : self.object,
                                                             'created' : datetime.date.today().strftime('%d.%m.%Y')})
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventCreationForm
    success_url = reverse_lazy("events:event_list")

    def form_valid(self, form):
        messages.success(self.request, 'Новое событие создано успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)

class EnrollCreationView(LoginRequiredMixin, CreateView):
    model = Enroll
    form_class = EnrollCreationForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, 'Вы записаны на событие')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)
        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_review'] = [review.user for review in self.object.reviews.all()]
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Событие {form.cleaned_data["title"]} измененно успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_update.html'
    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result

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







