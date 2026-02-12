from django.db import models
from django.contrib.auth.models import User

class Estimate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    square_footage = models.IntegerField()
    pound_estimate = models.IntegerField()
    crew_size = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Estimate {self.id} - {self.user.username}"
    
