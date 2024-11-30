from django.urls import path
from .views import PhoneAuthView, ProfileView, phone_auth_html

urlpatterns = [
    path('auth/', PhoneAuthView.as_view(), name='phone_auth'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('phone_auth_html/', phone_auth_html, name='phone_auth_html'),
]
