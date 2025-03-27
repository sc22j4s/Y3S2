import requests
from bs4 import BeautifulSoup
import json
import time
import string


import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')






BASE_URL = "https://quotes.toscrape.com/" # Takes to page 1


def scrape_page(url):
    """
    Returns parsed list of words from a webpage.
    """

    index = {}

    try:
        document = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    soup = BeautifulSoup(document.content, "html.parser")

    # Remove script and style elements
    for tag in soup(['script', 'style']):
        tag.extract()

     # Get visible text
    text = soup.get_text(separator=' ').lower()
    clean_text = text.translate(str.maketrans("", "", string.punctuation))
    words = clean_text.split()

    # Removing stopwords 
    for word in words:
        if word in stopwords.words('english'):
            words.remove(word)
    
    # Add words to inverted index
    return words





def build():
    """
    Crawls the website and builds an index
    Saves index to the file system (index.json)
    """

    index = {}
    authors = []
    url = BASE_URL # Goes to page 1
    filename = "index.json" # File to save index to
    page_list = []

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

        
        # Get all author links on page 
        author_links = soup.select('a[href^="/author/"]')
        
        for link in author_links:
            name = link["href"].split("/")[-1]
            # Avoid duplicate author page scraping
            if name not in authors:
                authors.append(name)
                url = f"{BASE_URL}{link['href']}"
                page_list.append(scrape_page(url))
        

        # Parse each page's content
        page_list.append(scrape_page(url, index))


        # Add words to inverted index
        
        # Navigate to next page (if exists)
        next = soup.find("li", class_="next")
        if next:
            # Update URL
            url = f"{BASE_URL}{next.a['href']}"
            print(url)
        else:
            break
        
   
    # Combine tokens into list of unique terms
    terms = list(set([term for page in page_list for term in page]))


    for term in terms:
        documents = []
   
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
        print("Usage: find <word1> <word2> ... <wordN>")
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