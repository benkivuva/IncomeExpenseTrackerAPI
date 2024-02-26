from django.shortcuts import render
from rest_framework import generics

class RegisterView(generics.GenericAPIView):
    
    def post(self, request):
        user = request.data