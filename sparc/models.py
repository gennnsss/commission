from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

# Role choices
ROLE_CHOICES = [
    ('Sales Agent', 'Sales Agent'),
    ('Sales Supervisor', 'Sales Supervisor'),
    ('Sales Manager', 'Sales Manager'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to built-in User model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Sales Agent')  # Default role
    is_approved = models.BooleanField(default=False)  # Admin must approve new users

    def __str__(self):
        return f"{self.user.username} - {self.role} - {'Approved' if self.is_approved else 'Pending'}"
