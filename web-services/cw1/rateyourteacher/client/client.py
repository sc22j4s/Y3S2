import requests
import json
import os

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


    response = requests.post(
        f"{URL}/register/", 
        data={"username": username,
               "email": email,
        "password": password})
    # response


    if response.status_code == 201:
        print("Successfully registered!")
    else:
        print("Registration failed. Please try again.")
        print(response.text)

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

    response = requests.post(
        f"{URL}/register/", 
        data={"username": username,
        "password": password})

    

    
    
    pass

def logout():
    pass

def list():
    pass

def average(args):
    if len(args) != 3:
        print("Usage: average <professor_id> <module_code>")
    pass

def rate(args):
    if len(args) != 6:
        print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
    pass


def main():
    print("Welcome to RateYourTeacher!")
    print("Type 'help' for command list, 'exit' to quit.")

    while True:
        inp = input(">>> ")
        
        args = inp.split(" ")
    
        if args[0] == "help":
            help()

        elif args[0] == "register":
            register()
        
        elif args[0] == "login":
            login(args)
        
        elif args[0] == "logout":
            logout() # may not need

        elif args[0] == "list":
            list(args)
        
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