from bs4 import BeautifulSoup as bs
import requests

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses
    return bs(response.text, 'html.parser')