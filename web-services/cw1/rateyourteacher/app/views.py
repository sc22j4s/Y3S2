from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from app.models import *

from pandas import DataFrame

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

        form_errors = []

        if not username:
            form_errors.append("Username missing")

        if not password:
            form_errors.append("Password missing")

        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is None and len(form_errors) == 0:
            form_errors.append("Invalid credentials") 

        # If any error messages, halt and return bad request signal
        if len(form_errors) > 0:
            # TODO concatenate
            errors = ""

            for i, error in enumerate(form_errors):
                errors += f"{i+1}. {error}\n"

            return JsonResponse({'message': errors}, status=401)
            
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

@csrf_exempt
@never_cache
def list(request):
    
    if request.method == "GET":
        instances = ModuleInstance.objects.all()
        data = []

        print("Instances:", instances)
        
        
        for instance in instances:
            # Query all ProfessorModule objects for this module instance
            professor_modules = ProfessorModule.objects.filter(module_instance=instance)
            
            
            # Build a list of professor representations (e.g., name and code)
            professor_list = [f"{pm.professor.name} ({pm.professor.code})" for pm in professor_modules]

            if professor_list == []:
                professor_list = "[None]"

            data.append({
                
                'Code': instance.module.code,
                'Name': instance.module.name,
                'Year': instance.year,
                'Semester': instance.semester,
                'Taught by': professor_list,

            })
        

        if len(data) == 0:
            return JsonResponse({'message': "Module instance data is empty."}, status=200)
        
        return JsonResponse(data, status=200, safe=False)
    
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

def view(request):
    
    if request.method == "GET":
        professors = Professor.objects.all()
        data = []

        for professor in professors:
            # Data formatting to two decimal places
            data.append(f"The rating for {professor.name} is {professor.rating:.2f}")

        if len(data) == 0:
            return JsonResponse({'message': "Professor data is empty."}, status=400)
        
        return JsonResponse(data, status=200, safe=False)

    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

def average(request):
    
    if request.method == "GET":
        professor = request.GET.get('professor_id')
        module = request.GET.get('module_code')

        if not professor:
            return JsonResponse({'message': "Professor ID is invalid"}, status=400)
        
        if not module:
            return JsonResponse({'message': "Module ID is invalid"}, status=400)
        
        
        # Query all ratings for this professor and module
        ratings = Rating.objects.filter(professor_module__professor_id=professor, professor_module__module_code=module)

        print(ratings)
        if len(ratings) == 0:
            return JsonResponse({'message': "No ratings found for this professor and module"}, status=404)
        
        average = sum([rating.rating for rating in ratings]) / len(ratings)
        average = f"{average:.2f}"
        
        return JsonResponse({'average': average}, status=200)
    
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)  


def rate(request):
    
    pass


