from rest_framework import serializers
from .models import Estimate

class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = '__all__'
        read_only_fields = ['user', 'price', 'created_at']