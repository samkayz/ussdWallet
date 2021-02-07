from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('log', views.log, name='log'),
    path('user', views.user, name='user'),
    path('logout', views.logout, name='logout'),
]