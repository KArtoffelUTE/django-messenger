from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('messages', MessageViewset, basename='message')
urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/create/', UserCreate.as_view(), name='user-create'),

    path('', include(router.urls)),
]