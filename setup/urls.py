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
from setup import settings
from merchant import urls
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', include('api.urls')),
    path('web/', include('web.urls')),
    path('merchant/', include('merchant.urls')),
    path('pay/v1/', include('pay.urls')),
    path('confirm', views.confirm, name='confirm'),
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('sendmoney', views.sendmoney, name='sendmoney'),
    path('history', views.history, name='history'),
    path('settings', views.settings, name='settings'),
    path('bankverify', views.bankverify, name='bankverify'),
    path('walletverify', views.walletverify, name='walletverify'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('terms-and-condition', views.terms_and_condition, name='terms-and-condition'),
    path('walletpay', views.walletpay, name='walletpay'),
]
