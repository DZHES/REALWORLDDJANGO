from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile
from django.http import HttpResponseRedirect
from events.models import Review

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
        profile = super().get_object(queryset)
        return profile

    def get(self, request, *args, **kwargs):
        if self.request.user.id == None:
            redirect_url = reverse_lazy('accounts:sign_in')
            return HttpResponseRedirect(redirect_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Profile.objects.filter(pk=self.kwargs['pk'])
        context['profile_reviews'] = [review.event for review in Review.objects.all()]
        return context

class CustomSignUpView(RedirectAuthenticatedUserMixin, CreateView):
    model = User
    template_name = 'accounts/registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return result

class CustomLoginView(RedirectAuthenticatedUserMixin, auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/signin.html'

