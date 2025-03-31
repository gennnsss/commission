from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  
    path('signin/', views.signin, name='signin'),  
    path('signout/', views.signout, name='signout'), 
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)