from web.views import home
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('transactions', views.transactions, name='transactions'),
    path('business_settings', views.business_settings, name='business_settings'),
    path('api_settings', views.api_settings, name='api_settings'),
]
