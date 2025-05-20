from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import generics, viewsets
from users.models import CustomUser
from users.serializers import CustomUserSerializer


# class CustomUserViewSet(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
#     lookup_field = 'email'


# POST
class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


# PATCH
class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'email'


# DELETE
class CustomUserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'email'


# GET
class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


# GET
class CustomUserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'email'
