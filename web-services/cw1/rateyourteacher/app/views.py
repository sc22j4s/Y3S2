from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from app.models import *

from email_validator import validate_email, EmailNotValidError
 

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

            """
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


            # Similar username / email check
            if User.objects.filter(username=username).exists():
                message.append("Username already exists")
        
            if User.objects.filter(email=email).exists():
                message.append("Email already exists")

            """
         
            # If any error messages, halt and return bad request signal
            if len(message) > 0:
                # TODO concatenate
                return JsonResponse({'message': message}, status=400)
            
            # Add to database using Django's User model
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Resource created (User), so return 201
            return JsonResponse({'message': "success"}, status=201)
        
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

@csrf_exempt
@never_cache
def login_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'message': "Missing username/password"}, status=400)
        


        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is None:
            return JsonResponse({'message': "Invalid credentials"}, status=401)

        login(request, authenticated_user)
        return JsonResponse({'message': "success"}, status=200)

    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

@csrf_exempt
@never_cache
def logout_user(request):
    print("asdfa")
    if request.method == "POST":   
        logout(request)
        return JsonResponse({'message': "success"}, status=200)
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

    

def list(request):
    pass

def average(request):
    pass

def rate(request):
    pass

