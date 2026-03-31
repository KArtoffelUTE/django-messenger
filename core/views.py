from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
# Create your views here.

class UserList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
