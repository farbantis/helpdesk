from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from account.forms import UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):

    template_name = 'account/user_login.html'
    form_class = UserLoginForm

    def get_redirect_url(self):
        """redirects user depending on role"""
        if self.request.user.is_staff:
            return '/admin_tasks/'
        else:
            return '/'


class RegisterUserView(CreateView):
    template_name = 'account/user_register.html'
    model = User
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.add_message(request, messages.SUCCESS, f'user was created')
            return redirect('account:login')
        else:
            form = UserRegistrationForm()
            messages.add_message(request, messages.ERROR, f'wrong data, please re-enter')
        return render(request, 'account/user_register.html', {'form': form})


class UserLogoutView(LogoutView):
    """logout user"""
    next_page = reverse_lazy('account:login')

