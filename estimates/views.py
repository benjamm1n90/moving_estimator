from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Estimate
from .serializers import EstimateSerializer
from .services import calculate_price

class EstimateListCreateView(generics.ListCreateAPIView):
    serializer_class = EstimateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Estimate.objects.all()

    def perform_create(self, serializer):
        square_feet = serializer.validated_data['square_footage']
        pounds = serializer.validated_data['pound_estimate']
        crew = serializer.validated_data['crew_size']

        price = calculate_price(square_feet, pounds, crew)

        serializer.save(user=self.request.user, price=price)
