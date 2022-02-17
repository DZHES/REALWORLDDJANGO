import datetime
from django.shortcuts import render, get_object_or_404
from events.models import Event, Review
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

def events_list(request):
    event_objects = Event.objects.all()
    context = {
        'event_objects' : event_objects
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event' : event,
        'display_places_left' : event.display_places_left()[0]
    }
    return render(request, 'events/event_detail.html', context)

@require_POST
def create_review(request):
    event_id = request.POST.get('event_id', '')
    rate = int(request.POST.get('rate', 0) or 0)
    text = request.POST.get('text', '')
    new_event = Event.objects.get(pk=int(event_id))

    data = {
        'ok' : True,
        'msg' : '',
        'rate' : int(rate),
        'text' : text,
        'created': datetime.date.today().strftime('%d.%m.%Y'),
        'user_name': request.user.__str__(),
    }

    if data['rate'] == '' or data['text'] == '':
        data['msg'] = 'Оценка и текст отзыва - обязательные поля'
        data['ok'] = False
        return JsonResponse(data)

    if not request.user.is_authenticated:
        data['msg'] = 'Отзывы могут оставлять только зарегистрированные пользователи'
        data['ok'] = False
        return JsonResponse(data)

    if Review.objects.filter(user=request.user, event=new_event).exists():
        data['msg'] = 'Вы уже отправляли отзыв к этому событию'
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







