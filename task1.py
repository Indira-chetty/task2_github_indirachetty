import os
import requests
import re
import sys  # Import sys module
from bs4 import BeautifulSoup

# function to get the html source text of the medium article
def get_page():
    global url
    
    url = input("Enter url of a medium article: ")  # Ask the user to input the URL of the Medium article and collect it in the variable 'url'
    
    # handling possible error
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid website, or make sure it is a Medium article')
        sys.exit(1)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    res = requests.get(url, headers=headers)  # Pass headers with User-Agent in the request
    
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub(r'<(.*?)>', '', text)  # Use raw string to handle HTML tags
    return text

def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    print(f"paragraphs text = \n {para_text}")
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

# function to save file in the current directory
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    print(name)
    fname = f'scraped_articles/{name}.txt'
    
    # Write a file using 'with' (2 lines)
    with open(fname, 'w') as f:
        f.write(text)

    print(f'File saved in directory {fname}')

if __name__ == '__main__':
    text = collect_text(get_page())
    save_file(text)
    # Instructions to run this Python code
    # Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
