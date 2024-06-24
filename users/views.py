from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm, LoginForm, ProfileConfigurate
from .models import Profile
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}')
            login(request, user)
            return redirect("users:configurate")
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.request.user.username})


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class ConfigurateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileConfigurate
    success_message = "Your profile is updated successfully"
    template_name = 'users/configurate_page.html'
    login_url = '/users/login/'

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    login_url = '/users/login/'

    def get_object(self):
        username = self.kwargs.get('username')
        if username == '<str:username>':
            username = self.request.user.username
        user = get_object_or_404(User, username=username)
        return get_object_or_404(Profile, user=user)
