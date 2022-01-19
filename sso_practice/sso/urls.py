import imp
from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, VerifyToken

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify/', VerifyToken.as_view(), name='verify')

]
