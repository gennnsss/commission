from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('signin/', views.signin, name='signin'),  
    path('signout/', views.signout, name='signout'), 
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
]
