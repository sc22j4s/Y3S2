from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer


# Create your views here
def index(request):
    template = loader.get_template('index.html')

    """
    Sign in, 
    """
    print("hello")
    return HttpResponse(template.render())

def register(request):
    
