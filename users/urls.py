from django.contrib import admin
from django.urls import path
from .views import SignUpView, SignInView, UserView, LogoutView, RefreshTokenView

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-in/', SignInView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh-token/', RefreshTokenView.as_view())
]