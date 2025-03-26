import requests
from bs4 import BeautifulSoup
import json
import time



BASE_URL = "https://quotes.toscrape.com/" # Takes to page 1


def scrape_page(url, index):

    pass



def build():
    """
    Crawls the website and builds an index
    Saves index to the file system (index.json)
    """

    index = {}
    authors = []
    url = BASE_URL # Takes to page 1
    filename = "index.json"

    while True:
            
        # Fetch each page
        try:
            
            document = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return
            
        # Six second politness policy
        # time.sleep(6)

        soup = BeautifulSoup(document.content, "html.parser")

        author_links = soup.select('a[href^="/author/"]')
        
        for link in author_links:
            name = link["href"].split("/")[-1]
            # Avoid duplicate author page scraping
            if name not in authors:
                authors.append(name)
                url = url = f"{BASE_URL}{next.a['href']}"
                scrape_page(url, index)
        
        print(authors)

        # Parse each page's content


        # Add words to inverted index
        
        # Navigate to next page (if exists)
        next = soup.find("li", class_="next")
        if next:
            # Update URL
            url = f"{BASE_URL}{next.a['href']}"
            print(url)
        else:
            break
        
   

   
    
  
        
    pass

def load():

    try:
        with open("index.json", "r") as file:
            index = json.load(file)
    except FileNotFoundError:
        print("Error: index.json not found. Run 'build' to create index.")
        return
    
    return



def print_index(args):
    
    if len(args) < 2:
        print("Usage: print <word>")
        return
    pass

def find(args):

    if len(args) < 2:
        print("Usage: find <word1> <word2> ... <wordN>")
        return
    

    pass


def main():
    print("WEB SERVICES - COURSEWORK 2")
    print("Type 'help' for command list, 'exit' to quit.")
    
    while True:

        try:
            response = requests.get(f"{BASE_URL}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        print("Server running")
    
        inp = input(">>> ").lower()
        args = inp.split()

        if len(args) == 0:
            continue
    
        elif args[0] == "build":
            build()

        elif args[0] == "load":
            index = load()
        
        elif args[0] == "print":
            print_index(args, index)

        elif args[0] == "find":
            find(args, index)

        elif args[0] == "exit":
            break
        
        else:
            print(f"Command {inp} not recognised. Type \"help\" for command list.")

    print("Exiting...") 
    

if __name__ == "__main__":
    main()