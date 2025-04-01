from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.home, name='home'),  
    path('navbar/', views.navbar, name='navbar'), 
    path('signin/', views.signin, name='signin'),  
    path('signout/', views.signout, name='signout'), 
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approve/', views.approve, name='approve'), 
    path('approve-user/<int:profile_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:profile_id>/', reject_user, name='reject_user'), # Admin view for user approval
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)