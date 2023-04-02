from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from account.api.resources import CreateUserAPIView, LogoutAPIView

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view()),
    path('login/', obtain_auth_token),
    path('logout/', LogoutAPIView.as_view()),
]
