import requests
import json
import os
from pandas import DataFrame

# URL = "sc22j4s@pythonanywhere.com"
URL = "http://127.0.0.1:8000"

"""
404 default error??

"""
def help():
    """
    Gets help textfile (from adjacent directory) and prints it.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    help_file = os.path.join(base_dir, "help.txt")
    try:
        with open(help_file, "r") as f:
            print(f.read())
            f.close()   
    except FileNotFoundError:
            print("Help file not found")  
    return

def register():
    # request to send prompts? 

    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")


    try:

        response = requests.post(
            f"{URL}/register/", 
            data={"username": username,
                "email": email,
            "password": password})

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    # response
    if response.status_code == 201:
        print("Successfully registered!")
        # login with details here?
    else:
        errors = response.json().get('message')
        print("Errors received from server:")
        print(errors)


    return

def login(args): 

    if len(args) != 2:
        print("Usage: login <url>")
        return
    
    url = args[1]
    url = URL # remove after deploying

    # check if URL exists
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        response = requests.post(
            f"{URL}/login_user/", 
            data={"username": username,
            "password": password})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        print("Successfully logged in!")
        return username
    elif response.status_code == 401:
        errors = response.json().get('message')
        print("Errors with sign-in:")
        print(errors)
    else:
        print("Login failed. Please try again.")
        print(response.text)
        return None


    return


def logout(name):

    if name == None:
        print("You are already not logged in.")
        return
    
    try:
        response = requests.post(
            f"{URL}/logout_user/",
            data={"username": name})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
        print("Successfully logged out!")   
        return None
    else:
        print("Logout failed. Please try again.")
        print(response.text)
        return name


def list():

    try:
        response = requests.get(f"{URL}/list/")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
    
        # check for empty list
        if response.json() == []:
            print("No module instances found.")
            return
        # to pandas dataframe
        df = DataFrame(response.json())
        print(df)

    else:
        print("Error retrieving list")
        print(response.text)

    return

def view():
    
    try:
        response = requests.get(f"{URL}/view/")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:

        # check for empty list
        if response.json() == []:
            print("No professors found.")
            return
        for professor in response.json():
            print(professor)

    pass

def average(args):

    if len(args) != 3:
        print("Usage: average <professor_id> <module_code>")
        return

    professor_id = args[1].upper()
    module_code = args[2].upper()

    try:
        response = requests.get(
            f"{URL}/average/",
            params={"professor_id": professor_id,
                "module_code": module_code})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
        professor = response.json().get('professor')
        module = response.json().get('module')
        rating = response.json().get('average')

        print(f"Average rating of {professor} on module \"{module}\": {rating}")
    elif response.status_code == 404:
        print("No ratings found for this professor and module.")
    else:
        print("Error retrieving average rating.")
        print(response.text)
    
    return

def rate(name, args):

    
    if len(args) != 6:
        print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")

    if name == None:
        print("You must be logged in to rate a professor.")
        return
    
    professor_id = args[1]
    module_code = args[2]
    year = args[3]
    semester = args[4]
    rating = args[5]
    
    try: 
        response = requests.post(
            f"{URL}/rate/", 
            data={"professor_id": professor_id,
                "module_code": module_code,
                "year": year,
                "semester": semester,
                "rating": rating})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
        print("Rating successful!")
    else:
        print("Rating failed.")
        print(response.text)
    pass


def main():
    print("Welcome to RateYourTeacher!") 
    print("Type 'help' for command list, 'exit' to quit.")
    name = None
    """TODO: use sessions instead of name"""

    while True:
        """
        if name == None:
            print("You are currently not logged in - type 'login <URL>' or 'register' to use the site.")
        else:
            print(f"Currently logged in as: {name}")
        """
        
        
        inp = input(">>> ").lower()
        
        
        args = inp.split(" ")
    
        if args[0] == "help":
            help()

        elif args[0] == "register":
            register()
        
        elif args[0] == "login":
            name = login(args)
        
        elif args[0] == "logout":
            name = logout(name)

        elif args[0] == "list":
            list()

        elif args[0] == "view":
            view()
        
        elif args[0] == "average":
            average(args)   

        elif args[0] == "rate":
            rate(name, args)
        
        elif args[0] == "exit":
            break

        else:
            print(f"Command {inp} not recognised. Type \"help\" for command list.")

    print("Exiting RateYourTeacher...") 


if __name__ == "__main__": 
    main()