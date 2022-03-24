from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from accounts.forms import (CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm,
                            CustomSetPasswordForm, CustomPasswordResetForm)
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile
from django.http import HttpResponseRedirect
from events.models import Review, Enroll
from allauth.account.views import LoginView
from django.db.models import Count, Sum, Q, Prefetch, F, Avg, DecimalField
from django.contrib import messages

class RedirectAuthenticatedUserMixin:
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main:index'))
        return super().get(*args, **kwargs)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_objects'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        self.kwargs['pk'] = pk
        queryset = super().get_queryset().filter(pk=pk)
        enroll = Enroll.objects.annotate(rate=Avg('event__reviews__rate', filter=Q(event__reviews__user=F('user')),
                                                  output_field=DecimalField()))
        prefetch_enroll = Prefetch('user__enrolls', enroll)
        queryset = queryset.select_related('user').prefetch_related(prefetch_enroll,'user__enrolls__event',
                                                                    'user__reviews__event', 'user__reviews')
        profile = super().get_object(queryset)
        return profile

    def get(self, request, *args, **kwargs):
        if self.request.user.id == None:
            redirect_url = reverse_lazy('accounts:sign_in')
            return HttpResponseRedirect(redirect_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomSignUpView(RedirectAuthenticatedUserMixin, CreateView):
    model = User
    template_name = 'accounts/registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные обновлены')
        result = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return result

# class CustomLoginView(RedirectAuthenticatedUserMixin, auth_views.LoginView):
#     form_class = CustomAuthenticationForm
#     template_name = 'accounts/registration/signin.html'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/signin.html'

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/registration/password_reset_email.txt'
    subject_template_name = 'accounts/registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    html_email_template_name = 'accounts/registration/password_reset_email.html'
    from_email = 'mr.sirius1997@mail.ru'

    def form_valid(self, form):
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')
        return context

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'