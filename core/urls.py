from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('messages', MessageViewset, basename='message')
router.register('users', UserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
]