from django.urls import path, re_path
from . import views


urlpatterns = [
    path('initiate', views.initiate, name='initiate'),
    path('final/<token>', views.final, name='final')
]
