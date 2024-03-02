from rest_framework import serializers
from .models import CustomUser # Import your custom user model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Use your custom user model here
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'sec_answer', 'username']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user