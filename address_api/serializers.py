from rest_framework import serializers
from .models import ValidAddress




class ValidAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidAddress
        fields = ['id', 'currency', 'address', 'public_key']
