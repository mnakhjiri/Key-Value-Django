from rest_framework import serializers
from .models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAccount
        fields = ('email', 'first_name', 'last_name', 'joined', 'password')
        read_only_fields = ('joined',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        return user
