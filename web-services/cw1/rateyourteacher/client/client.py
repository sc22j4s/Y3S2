# import requests
import json
import os

# URL = "sc22j4s@pythonanywhere.com"
URL = "127.0.0.1"


def register():
    pass

def help():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    help_file = os.path.join(base_dir, "help.txt")
    try:
        with open(help_file, "r") as f:
            print(f.read())
            f.close()   
    except FileNotFoundError:
            print("Help file not found")  



def main():
    print("Welcome to RateYourTeacher!\n")
    print("Type 'help' for command list")

    while True:
        inp = input(">>> ")
        
        args = inp.split(" ")
    
        if args[0] == "help":
            
            help()
        elif args[0] == "register":
            pass


    
        else:
            print(f"Command {inp} not recognised. Type \"help\" for command list.")

if __name__ == "__main__": 
    main()