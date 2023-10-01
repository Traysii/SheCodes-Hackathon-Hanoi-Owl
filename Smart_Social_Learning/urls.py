from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Result.as_view(), name= 'main'),
    path('login', Login.as_view(), name= 'login'),
    path('logout', LogoutView.as_view(next_page = 'login'), name= 'logout'),
    path('register', Register.as_view(), name= 'register'),
]