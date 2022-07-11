from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'user'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/history/', order_history, name='history'),
]