from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from app.models import *

from email_validator import validate_email, EmailNotValidError
 


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
            
            form_errors = []

            print(f"{username} {email} {password}")
            if len(username) < 8 or len(username) > 20:
                if len(username) == 0:
                    form_errors.append("Username cannot be empty")
                else:
                    form_errors.append("Username must be between 8 and 20 characters")
            
            if len(password) < 8 or len(password) > 20:
                if len(password) == 0: 
                    form_errors.append("Password cannot be empty")
                else:
                    form_errors.append("Password must be between 8 and 20 characters")

            # Email validation (from package)
            try:
                email_info = validate_email(email)  
                email = email_info.normalized 
            except EmailNotValidError as e:  
                form_errors.append(str(e))  # Get specific email error from library

           
            # Similar username / email check
            if User.objects.filter(username=username).exists():
                form_errors.append("Username already associated with another account")
        
            if User.objects.filter(email=email).exists():
                form_errors.append("Email already associated with another account")

            

            # If any error messages, halt and return bad request signal
            if len(form_errors) > 0:
                # TODO concatenate
                errors = ""

                for i, error in enumerate(form_errors):
                    errors += f"{i+1}. {error}\n"

                return JsonResponse({'message': errors}, status=400)
            
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

        # Django built-in login function
        login(request, authenticated_user)
        return JsonResponse({'message': "success"}, status=200)

    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

@csrf_exempt
@never_cache
def logout_user(request):

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

