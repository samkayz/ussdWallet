from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', views.signup, name='signup'),
    path('account/<mobile>', views.account, name='account'),
    path('transfer/<mobile>', views.transfer, name='transfer'),
    path('accountVerify', views.accountVerify, name='accountVerify'),
    path('btranfer/<mobile>', views.btranfer, name='btranfer'),
    path('getData/<scode>', views.getData, name='getData'),
    path('buyAirtime/<mobile>', views.buyAirtime, name='buyAirtime'),
]
