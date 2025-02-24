from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from app.models import *


from email_validator import validate_email, EmailNotValidError

# Create your views here
def index(request):
    template = loader.get_template('index.html')

    """
    Sign in, 
    """
    print("hello")
    return HttpResponse(template.render())

def test(request):
    
    print("lol")
    return HttpResponse("FUCK YOU")

@csrf_exempt
@never_cache 
def register(request):
    """
    TODO:
    figure out status codes
    """
    
    if request.method == 'POST':
        try:
            
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password') 
            
            message = []

            if len(username) < 8 or len(username) > 20:
                message.append("Username must be between 8 and 20 characters")
            
            if len(password) < 8 or len(password) > 20:
                message.append("Password must be between 8 and 20 characters")

            # Email validation (from package)
            try:
                email_info = validate_email(email)  
                email = email_info.normalized 
            except EmailNotValidError as e:  
                message.append(str(e))  # Get specific email error from library

            # If any error messages, halt and return bad request signal
            if len(message) > 0:
                # TODO concatenate
                return JsonResponse({'message': message}, status=400)
            
            # Add to database
            user = User(username=username, password=password, email=email)
            user.save()

            # Resource created (User), so return 201
            print("success")
            return JsonResponse({'message': "success"}, status=201)
        
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

@csrf_exempt
@never_cache
def login(request):

    if request.method == "POST":
        
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.get(username=username, password=password)

            if user is None:
                return JsonResponse({'message': "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

def logout(request):
    pass

def list(request):
    pass

def average(request):
    pass

def rate(request):
    pass

