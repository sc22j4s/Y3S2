from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

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
def register(request):
    """
    TODO:
    figure out status codes
    """
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        
        message = []

        if len(username) < 8 or len(username) > 20:
            message.append("Bad username")
        
        if len(password) < 8 or len(password) > 20:
            message.append("Bad password")
    
        try:
            email_info = validate_email(email)  # validate and get email info
            email = email_info.normalized  # validates the address and gives you its normalized form
            print(f'{email} is valid')  # print success message
        except EmailNotValidError as e:  # catch invalid emails
            message.append(f'{email} is not valid')  # print failure message
            print(str(e))  # print the specific error message

        # If any error messages, halt and return issues
        if len(message) > 0:
            # TODO concatenate
            return JsonResponse({'message': message})
        
        # Add to database
        user = User(username=username, password=password, email=email)
        user.save()

        return JsonResponse({'message': "success"})
        
    
    else:

        return JsonResponse({'message': "Incorrect request method"})

def login(request):
    pass

def logout(request):
    pass

def list(request):
    pass

def average(request):
    pass

def rate(request):
    pass

