from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from mail.models import Subscriber, Letter
from realworlddjango.settings import EMAIL_HOST_USER
from django.urls import reverse
from threading import Thread

@require_POST
def create_letters_view(request):
    emails = request.POST.getlist('email', None)
    subject = request.POST.get('subject', '')
    text = request.POST.get('text', '')
    if emails and subject and text:
        Letter.create_letters(emails, subject, text)

    return JsonResponse({'subscribers': Subscriber.get_objects_list()})

@require_POST
def send_letters(request):
    unsent_letters = Letter.objects.filter(is_sent=False)
    for letter in unsent_letters:
        th = Thread(target=lambda: send_mail(
            subject=letter.subject,
            message=letter.text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[letter.to.email],
            fail_silently=False))
        th.start()
        letter.is_sent = True
        letter.save()

    return HttpResponseRedirect(reverse('mail:subscriber_list'))

def get_subscribers(request):
    all_emails_sent = not Letter.objects.filter(is_sent=False).exists()
    return JsonResponse({'subscribers': Subscriber.get_objects_list(),
                         'all_emails_sent': all_emails_sent})
