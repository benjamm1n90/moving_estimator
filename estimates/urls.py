from django.urls import path
from .views import EstimateListCreateView

urlpatterns = [
    path('estimates/', EstimateListCreateView.as_view(), name='estimates'),
]
