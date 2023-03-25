from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User
from account.forms import UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    """logging user"""
    template_name = 'account/user_login.html'
    form_class = UserLoginForm
    # next_page = 'cafe:main_page'

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        if self.request.user.is_staff:
            pass
            # redirect_to = '/admin_panel/'
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
        return render(request, 'account/user_register.html', {'form': form})


class UserLogoutView(LogoutView):
    """logout user"""
    #next_page = reverse_lazy('cafe:main_page')
#
#
# class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
#     template_name = 'account/change_password.html'
#     success_url = reverse_lazy('cafe:user_dashboard')
#     success_message = 'Пароль пользователя изменен'
#
#
# class UserPasswordChangeDoneView(PasswordChangeDoneView):
#     pass
