from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    email= serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = ('id','username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields don't match"})
        return attrs

    def create(self, validated_data):
        user = Profile.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
