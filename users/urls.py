from django.urls import path
from .views import UserCreateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('sign-up/', UserCreateView.as_view(), name='sign-up'),
    path('sign-in/', obtain_auth_token, name='sign-in'),  # DRF built-in view for obtaining tokens
]