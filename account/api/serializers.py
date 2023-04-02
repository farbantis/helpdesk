from rest_framework import serializers
from account.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password1')
        # extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password1 = attrs.pop('password1', None)

        if password != password1:
            raise serializers.ValidationError("Passwords don't match")
        return attrs


