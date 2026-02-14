from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Estimate

class EstimateAPITestCase(APITestCase):

    def test_authenication_required(self):
        url = reverse('estimate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_estimate(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        url = reverse('estimate-list')
        data = {
            'square_footage': 1000,
            'pound_estimate': 5000,
            'crew_size': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estimate.objects.count(), 1)
        estimate = Estimate.objects.first()
        self.assertEqual(estimate.user, user)
        self.assertEqual(estimate.square_footage, 1000)
        self.assertEqual(estimate.pound_estimate, 5000)
        self.assertEqual(estimate.crew_size, 3)
    
    def test_users_cannot_see_eachothers_estimates(self):
        user1 = User.objects.create_user(username='testuser1', password='testpass1')
        user2 = User.objects.create_user(username='testuser2', password='testpass2')

        Estimate.objects.create(
            user=user1,
            square_footage=1000,
            pound_estimate=8000,
            crew_size=3,
            price=2500
        )

        self.client.login(username='testuser2', password='testpass2')
        url = reverse('estimate-list')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 0)

    def test_invalid_weight_fails(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        url = reverse('estimate-list')

        data = {
            "square_footage": 1000,
            "pound_estimate": -500,
            "crew_size": 3
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    