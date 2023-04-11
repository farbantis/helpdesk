from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from account.models import User


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'login_username_inner', 'placeholder': 'username'})
        self.fields['password'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'password'})


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'repeat password'})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
