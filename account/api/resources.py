from django.contrib.auth import logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from account.api.serializers import CreateUserSerializer
from account.models import User


# class UserAuthToken(ObtainAuthToken):
#     def get_success_url(self):
#         pass


class CreateUserAPIView(CreateAPIView):
    """creates an instance of a helpdesk User"""
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    http_method_names = ['post']


class LogoutAPIView(APIView):
    """logs out user"""
    def post(self, request):
        logout(request)
