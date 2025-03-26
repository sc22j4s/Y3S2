import getpass
import os
from pandas import DataFrame
import requests

URL = "https://sc22j4s.pythonanywhere.com"

# Persistent session - storing token in headers.
session = requests.Session()

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

    # Get user details
    username = input("Enter username: ")
    email = input("Enter email: ")

    # Password match
    while True:
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")

    # Post request to server
    try:
        response = session.post(
            f"{URL}/register/", 
            data={"username": username,
                "email": email,
            "password": password})
    # Generic error handling for when server is not running
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    # response
    if response.status_code == 201:
        print("Successfully registered!")
        # login with details here?
    elif response.status_code == 400:
        # Form parsing errors 
        errors = response.json().get('message')
        print("Errors received from server:")
        print(errors)
    elif response.status_code == 409:
        # Conflict - user/email already exists
        print(f"{response.json().get('conflict')} already exists.")
    else:
        print("Registration failed. Please try again.")
        print(response.text)
        
    return

def login(args): 

    if len(args) != 2:
        print("Usage: login <url>")
        return

    # Per specification, URL shouldn't need "https://"
    url = args[1]

    # Corrects URL if not already
    if not url.startswith('https://'):
        url = f"https://{url}"

        
    # Check if URL exists
    try:
        response = session.get(url)
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    try:
        response = session.post(
            f"{URL}/login_user/", 
            data={"username": username,
            "password": password})
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        print("Successfully logged in!")
    elif response.status_code == 401:
        errors = response.json().get('message')
        print("Errors with sign-in:")
        print(errors)
    elif response.status_code == 500:
        print("Server error occurred. Please try again.")
    else:
        print("Login failed. Please try again.")
        print("Code: " + response.status_code)
        return None


    return


def logout():
    """
    Removes authentication token from session header.
    (If it exists already)
    """

    # Check if user is already logged in
    if not session.cookies.get("sessionid"):
        print("You are already not logged in.")
        return

    try: 
        response = session.post(f"{URL}/logout_user/") 
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    if response.status_code == 200:
        # Remove local authentication state
        session.cookies.clear()
        print("Successfully logged out!")
    elif response.status_code == 401:
        print("Server error occurred. Please try again.")
    elif response.status_code == 500:
        print("Server error occurred. Please try again.")
    else:
        print("Logout failed.")
        print(response.text) 

    return
        

def list():
    """
    Gets a list of all module instances, with professors teaching them.
    Each entry can be voted on by logged in users.
    """

    try:
        response = session.get(f"{URL}/list/")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
        # OK - convert list to pandas dataframe
        df = DataFrame(response.json())
        print(df)
    elif response.status_code == 204:
        # No content
        print("Module instance database is empty.")
    elif response.status_code == 500:
        print("Server error occurred. Please try again.")
    else:
        # Generic error
        print("Unknown error retrieving list.")
        
        

    return

def view():
    """
    Gets a list of all professors with their average ratings,
    across all module instances.
    """
    
    try:
        response = session.get(f"{URL}/view/")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
        for professor in response.json():
            print(professor)
    elif response.status_code == 204:
        # No content
        print("Professor database is empty.")
    elif response.status_code == 500:
        print("Server error occurred. Please try again.")
    else:
        print("Error retrieving professors.")


def average(args):

    if len(args) != 3:
        print("Usage: average <professor_id> <module_code>")
        return

    professor_id = args[1].upper()
    module_code = args[2].upper()

    try:
        response = session.get(
            f"{URL}/average/",
            params={"professor_id": professor_id,
                "module_code": module_code})
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    # Expected response 
    if response.status_code == 200:
        professor = response.json().get('professor')
        module = response.json().get('module')
        rating = response.json().get('average')

        print(f"Average rating of {professor} on module \"{module}\": {rating}")

    elif response.status_code == 400:
        # Bad request - print errors returned
        print(response.json().get('message'))  
    elif response.status_code == 404:
        # Module / professor does not exist in database
        print(response.json().get('message'))
    elif response.status_code == 500:
        print("Server error occurred. Please try again.")
    else:
        print("Unknown error retrieving average rating.")
        print(response.text)
    
    return

def rate(args):

    if len(args) != 6:
        print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
        return

    # Alphanumeric inputs are capitalised for sanitisation
    professor_id = args[1].upper()
    module_code = args[2].upper()
    year = args[3]
    semester = args[4]
    rating = args[5]
    
    # Post request to server
    try: 
        response = session.post(
            f"{URL}/rate/", 
            data={"professor_id": professor_id,
                "module_code": module_code,
                "year": year,
                "semester": semester,
                "rating": rating,
            }
        )
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - check URL and try again.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    if response.status_code == 200:
        # Rating already exists, so update it
        professor = response.json().get('professor')  
        module = response.json().get('module')
        print(f"[Updated] {professor} {rating} stars on module \"{module}\".")

    elif response.status_code == 201:
        # New rating created
        professor = response.json().get('professor')  
        module = response.json().get('module')
        print(f"[Gave] {professor} {rating} stars on module \"{module}\".")

    elif response.status_code == 400:
        # Errors in user input
        errors = response.json().get('message')
        print("Errors received from server:")
        print(errors)
    elif response.status_code == 401:
        # User not logged in
        print("You must be logged in to rate professors.")
    elif response.status_code == 404:
        # Query data empty from database
        print(response.json().get('message'))
    elif response.status_code == 500:
        print("Server error occurred. Please try again.")
    else:
        print("Unkown error rating professor.")
        print(response.text)

    return


def main():

    try:
        response = session.get(f"{URL}/test/")
        # Welcome message from server
        print(f"Connected to {URL}.")
        if response.status_code == 200:
            print(response.json().get('message')) 
    except requests.exceptions.ConnectionError:
        # Applcation is not usable - warn in advance
        print("Could not connect to server - it may be offline or the default URL is invalid.")
        

    print("Type 'help' for command list, 'exit' to quit.")
    
    while True:

        try:
            response = session.get(f"{URL}/get_username/")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return
        
        if response.status_code == 200:
            print(f"Currently logged in as: {response.json().get('username')}")    
        elif response.status_code == 401:
            print("You are currently not logged in - type register or login <URL> to rate professors.")
        elif response.status_code == 500:
            print("Server error occurred. Please try again.")
        else:
            print("Error retrieving username.")
            print(response.text)
            
        print()
    
        inp = input(">>> ").lower()
        args = inp.split()

        if len(args) == 0:
            continue
    
        elif args[0] == "help":
            help()

        elif args[0] == "register":
            register()
        
        elif args[0] == "login":
            login(args)
        
        elif args[0] == "logout":
            logout()

        elif args[0] == "list":
            list()

        elif args[0] == "view":
            view()
        
        elif args[0] == "average":
            average(args)   

        elif args[0] == "rate":
            rate(args)
        
        elif args[0] == "exit":
            break

        else:
            print(f"Command {inp} not recognised. Type \"help\" for command list.")

    print("Exiting RateYourTeacher...") 

if __name__ == "__main__": 
    main()