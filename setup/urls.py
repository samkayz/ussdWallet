"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from merchant import urls
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', include('api.urls')),
    path('web/', include('web.urls')),
    path('merchant/', include('merchant.urls')),
    path('confirm', views.confirm, name='confirm'),
    path('', views.index, name='index'),
    path('landing', views.landing, name='landing'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
]
