from django.contrib import admin
from django.urls import path
from .views import SignUpView, SignInView, UserView, LogoutView

urlpatterns = [
    path('sign_up/', SignUpView.as_view()),
    path('sign_in/', SignInView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
]