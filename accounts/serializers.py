from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('password', 'email', 'name')


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=20, write_only=True, required=True)
    email = serializers.EmailField(
        write_only=True, required=True, allow_blank=False)

    def custom_signup(self, request, user):
        name = self.validated_data.pop("name")
        if name:
            user.name = name
        user.save()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'email', 'name')
        read_only_fields = ('email', )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return super().update(instance, validated_data)
