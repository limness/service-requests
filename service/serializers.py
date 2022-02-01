
from rest_framework import serializers

from .models import User, DiagnosticRequest


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=128, min_length=8, write_only=True)
    car = serializers.CharField(max_length=16, min_length=2, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegistrationSerializer(serializers.ModelSerializer):

    expert = serializers.CharField(max_length=128, min_length=8, write_only=True)
    time = serializers.DateTimeField(write_only=True)

    class Meta:
        model = DiagnosticRequest
        fields = ('__all__')
