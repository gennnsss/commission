from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model
from django.db.models import Sum



class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_sales(self):
        """Calculate total sales for the entire team"""
        return Sale.objects.filter(agent__team=self).aggregate(Sum('price'))['price__sum'] or 0

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('Sales Agent', 'Sales Agent'),
        ('Sales Supervisor', 'Sales Supervisor'),
        ('Sales Manager', 'Sales Manager'),
    ], default='Sales Agent')
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_pics/', default='media/default.png')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="agents")

    def total_sales(self):
        return self.sales.aggregate(Sum('price'))['price__sum'] or 0

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.team.name if self.team else 'No Team'}"
    
class Sale(models.Model):
    property_id = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    agent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sales')

    def __str__(self):
        return f"{self.property_name} - ₱{self.price:,}"
    

