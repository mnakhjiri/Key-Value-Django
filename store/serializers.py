from rest_framework import serializers
from .models import StoreValue


class StoreValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreValue
        fields = ('key', 'value')
