from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

urlpatterns = [
    path("signin/",TokenObtainPairView.as_view(),name="token_obtain_pair"), #토큰으로 access토큰 필요
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #access 토큰 만료되면 refresh토큰으로 access토큰 만들어야하니까까
]
