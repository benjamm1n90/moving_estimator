from rest_framework import serializers
from .models import Estimate

class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = '__all__'
        read_only_fields = ['user', 'price', 'created_at']

    def validate_pound_estimate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be positive.")
        return value

    def validate_crew_size(self, value):
        if value <= 0:
            raise serializers.ValidationError("Crew size must be greater than 0.")
        return value
