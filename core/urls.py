from django.urls import path
from .views import *


urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/create/', UserCreate.as_view(), name='user-create'),
]