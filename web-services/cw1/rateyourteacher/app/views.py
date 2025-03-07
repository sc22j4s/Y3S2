from app.models import *

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from email_validator import validate_email, EmailNotValidError
 

@csrf_exempt
@never_cache 
def test(request):
    """
    Test endpoint to check if server is running,
    and send a welcome message.
    """
    return JsonResponse({'message': "Welcome to RateYourTeacher!"}, status=200)


@csrf_exempt
@never_cache 
def get_username(request):
    """
    Takes user session token and returns the username associated with it.
    Requested after every action (so username is refreshed properly).
    """
    if request.method == "GET":
        # Catch for unauthenticated users
        try:  
            if request.user.is_authenticated:
                username = request.user.username
                return JsonResponse({'message': "success", 'username': username}, status=200)
            else:
                return JsonResponse({'message': "No user logged in"}, status=401)
        except:
            return JsonResponse({'message': "Internal server error"}, status=500)
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)
    
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
                return JsonResponse({'message': "Username already associated with another account",
                                     'conflict': "Username"}, status=409)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': "Email already associated with another account",
                                     'conflict': "Email"}, status=409)

            # If any error messages, halt and return bad request signal
            if len(form_errors) > 0:
                errors = ""

                for i, error in enumerate(form_errors):
                    errors += f"{i+1}. {error}\n"

                return JsonResponse({'message': errors}, status=400)
            
            # Add to database using Django's User model
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
            except:
                return JsonResponse({'message': "Internal server error"}, status=500)

            # Resource created (User), so return 201
            return JsonResponse({'message': "success"}, status=201)
        
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
        except:
            return JsonResponse({'message': "Internal server error"}, status=500)
    
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)

@csrf_exempt
@never_cache
def login_user(request):
    """
    Login endpoint for users.
    Calls Django's built-in authenticate and login functions.
    """

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        form_errors = []

        # Build list of possible form errors
        if not username:
            form_errors.append("Username missing")

        if not password:
            form_errors.append("Password missing")

        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is None and len(form_errors) == 0:
            form_errors.append("Invalid credentials") 

        # If any error messages, halt and return bad request signal
        if len(form_errors) > 0:
            errors = ""

            for i, error in enumerate(form_errors):
                errors += f"{i+1}. {error}\n"

            return JsonResponse({'message': errors}, 
                                status=401)
            
        # Django built-in login function
        try:
            login(request, authenticated_user)
        except:
            return JsonResponse({'message': "Internal server error"}, 
                                status=500)
        return JsonResponse({'message': "success"}, 
                            status=200)

    else:
        return JsonResponse({'message': "Incorrect request method"}, 
                            status=405)

@csrf_exempt
@never_cache
def logout_user(request):
    """
    Logout endpoint for users.
    Calls Django's built-in logout function.
    """

    if request.method == "POST":   

        if not request.user.is_authenticated:
            return JsonResponse({'message': "User is not authenticated"}, status=401)
    
        try:    
            logout(request)
            return JsonResponse({'message': "success"}, 
                                status=200)
        except Exception as e:
            return JsonResponse({'message': 'Internal server error'}, status=500)

    
    else:
        return JsonResponse({'message': "Incorrect request method"}, 
                            status=405)

@csrf_exempt
@never_cache
def list(request):
    """
    Lists all module instances and their associated professors which teach them.
    """

    if request.method == "GET":

        # Query all ModuleInstance objects from database
        instances = ModuleInstance.objects.all()
        data = []
        
        for instance in instances:
            # Query all ProfessorModule objects for this module instance 
            try:
                professor_modules = ProfessorModule.objects.filter(module_instance=instance)
            except:
                return JsonResponse({'message': "Internal server error"}, 
                                    status=500)
    
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
            return JsonResponse({'message': "Module instance data is empty."}, 
                                status=204)
        
        # Safe tag to allow for non-dictionary JSON objects
        return JsonResponse(data, status=200, safe=False)
    
    else:
        return JsonResponse({'message': "Incorrect request method"}, 
                            status=405)

@csrf_exempt
@never_cache
def view(request):
    
    if request.method == "GET":
        try:
            professors = Professor.objects.all()
        except:
            return JsonResponse({'message': "Internal server error"},
                                status=500)
    
        data = []
        if len(data) == 0:
            return JsonResponse({'message': "Professor data is empty."}, 
                                status=204)

        for professor in professors:
            # Data formatting to two decimal places
            data.append(f"The rating for {professor.name} is {professor.rating:.2f}")

        return JsonResponse(data, status=200, safe=False)

    else:
        return JsonResponse({
            'message': "Incorrect request method"
        }, status=405)
                            
@csrf_exempt
@never_cache
def average(request):
    
    if request.method == "GET":

        print("sdujnfisdjfnsikdjnf")
        
        # Get data from query
        professor = request.GET.get('professor_id')        
        module = request.GET.get('module_code')

        # Input handling
        if not professor:
            return JsonResponse({'message': "Professor ID is invalid"}, 
                                status=400)
        
        if not module:
            return JsonResponse({'message': "Module ID is invalid"}, 
                                status=400)
        
       
        try:
            # Return actual names for user readability
            professor_name = Professor.objects.filter(code=professor).first()
            print(professor_name)
            if not professor_name:
                return JsonResponse({'message': "Professor not found"}, 
                                    status=404)
            
            module_name = Module.objects.filter(code=module).first()
            print(module_name)
            if not module_name:
                return JsonResponse({'message': "Module not found"}, 
                                    status=404)
            

            # Query all ratings for this professor and module
            ratings = Rating.objects.filter(professor_module__professor__code=professor,
                                            professor_module__module_instance__module__code=module)
        except:
            return JsonResponse({'message': "Internal server error"}, 
                                status=500)
    
        if len(ratings) == 0:
            return JsonResponse({'message': "No ratings found for this professor and module"}, 
                                status=404)

        average = sum([rating.rating for rating in ratings]) / len(ratings)
        average = f"{average:.2f}"

        return JsonResponse({
            'professor': str(professor_name), 
            'module': str(module_name), 
            'average': average
        }, status=200)
                           
    else:
        return JsonResponse({'message': "Incorrect request method"}, status=405)  

@csrf_exempt
@never_cache
def rate(request):

    if request.method == "POST":

        if not request.user.is_authenticated:
            return JsonResponse({'message': "User not authenticated"}, status=401)
        
        # Get data from query
        professor = request.POST.get('professor_id')
        module = request.POST.get('module_code')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        rating = request.POST.get('rating')

        request_errors = []

        # Input handling
        if not professor:
            request_errors.append("Professor ID is missing")
        if not module:
            request_errors.append("Module ID is missing")
        if not year:
            request_errors.append("Year is missing")
        elif not year.isnumeric():
            request_errors.append("Year input is invalid")
        
        if semester not in ['1', '2']:
            request_errors.append("Semester must be 1 or 2")
        elif not semester:
            request_errors.append("Semester is missing")
        
        if rating not in ['1', '2', '3', '4', '5']:
            request_errors.append("Rating must be an integer between 1 and 5")
        elif not rating:
            request_errors.append("Rating is missing")
        
        # Check for bad request
        if len(request_errors) > 0:
            errors = ""

            for i, error in enumerate(request_errors):
                errors += f"{i+1}. {error}\n"

            return JsonResponse({'message': errors}, status=400)
        
        # Return actual names for user readability
        user = request.user
        
        # Database querying:
        try:
            # Check if professor exists:
            professor_obj = Professor.objects.filter(code=professor).first()
            if not professor_obj:
                return JsonResponse({'message': "Professor not found"}, status=404) 
            
            professor_name = Professor.objects.filter(code=professor).first()
            
            # Check if module exists:
            module_obj = Module.objects.filter(code=module).first()
            if not module_obj:
                return JsonResponse({'message': "Module not found"}, status=404)
            
            module_name = Module.objects.filter(code=module).first()

            # Check if module instance exists:
            module_instance = ModuleInstance.objects.filter(module=module_obj, year=year, semester=semester).first()
            if not module_instance:
                return JsonResponse({'message': f"Module {str(module_name)} exists, but no instances match the query. Check the year and semester."},
                                    status=404)
            
            # Check if professor is associated with module instance
            professor_module = ProfessorModule.objects.filter(professor=professor_obj, module_instance=module_instance).first()
            if not professor_module:
                return JsonResponse({'message': f"Professor {str(professor_name)} not associated with this module instance."},
                                    status=404)

            # Check if rating already exists
            existing_rating = Rating.objects.filter(
                user=user,
                professor_module__professor=professor_obj,
                professor_module__module_instance=module_instance
            ).first()

        except:
            return JsonResponse({'message': "Internal server error"}, status=500)

        if existing_rating:
            existing_rating.rating = rating
            existing_rating.save()

            return JsonResponse(
                {'message': "Rating updated",
                 'professor': str(professor_name),
                 'module': str(module_name)}, 
            status=200)
        else:
            # Create new rating
            new_rating = Rating(user=user, professor_module=professor_module, rating=rating)
            new_rating.save()
            return JsonResponse(
                {'message': "Rating created",
                 'professor': str(professor_name),
                 'module': str(module_name)}, 
            status=201)
            
        




       
        




