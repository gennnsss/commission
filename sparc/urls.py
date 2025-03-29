from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),  
    path('signin/', views.signin, name='signin'),  
    path('signout/', views.signout, name='signout'), 
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approve/', views.approve, name='approve'), 
    path('approve-user/<int:profile_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:profile_id>/', reject_user, name='reject_user'), # Admin view for user approval
]
