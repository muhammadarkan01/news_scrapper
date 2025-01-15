import pandas
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import logging

# Setup Logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("error.log")
file_handler.setLevel(logging.ERROR)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_soup(url):
    response = requests.get(url)
    text_response = response.text
    soup = bs(text_response, 'html.parser')

    return soup

def date_converter(date_raw):
    date_string_cleaned = date_raw.split(",")[1].strip().replace("WIB", "").strip()
    date = datetime.strptime(date_string_cleaned, '%d %b %Y %H:%M')

    return date

def get_article(url):
    try:
        soup = get_soup(url)
        content = soup.find('div', class_='column-8')

        # Extract title
        title = content.find('h1', class_='detail__title').text.strip() if content and content.find('h1', class_='detail__title') else None

        # Extract author
        author = content.find('div', class_='detail__author').text.strip() if content and content.find('div', class_='detail__author') else None

        # Extract date
        date = None
        if content and content.find('div', class_='detail__date'):
            date_raw = content.find('div', class_='detail__date').text
            date = date_converter(date_raw)

        # Extract article content
        paragraphs = []
        if content:
            paragraphs_content = content.find_all('p')
            for p in paragraphs_content:
                paragraphs.append(p.text.strip())
        
        article = " ".join(paragraphs) if paragraphs else None

        # Log error if any field is missing
        if not title or not author or not article:
            logger.error(f"Missing content for page: {url}")
        
        return title, author, date, article
    except Exception as e:
        logger.error(f"Error occurred while scraping {url}: {e}")
        return None, None, None, None

def save_articles_to_csv(articles, filename="articles.csv"):
    try:
        df = pandas.DataFrame(articles)
        df.to_csv(filename, index=False)
        logger.info(f"Articles successfully saved to {filename}")
    except Exception as e:
        logger.error(f"Error occurred while saving articles to CSV: {e}")

articles = []
date_now = datetime.now()
date = datetime.now()
i = 1

status = True

while status:
    url = f'https://oto.detik.com/indeks?page={i}'
    logger.info(f"Scraping page: {url}")
    soup = get_soup(url)
    news_contents = soup.find_all('article', class_='list-content__item')

    for content in news_contents:
        link = content.find('a')['href']

        date_raw = content.find('div', class_='media__date').find('span')['title']
        date = date_converter(date_raw)

        date_delta = date_now - date
        date_delta = date_delta.seconds/60

        if date_delta < 60.0:
            logger.info(f"Scraping article: {link}")
            title, author, date, article = get_article(link)
            if title and article:  # Append only if there's valid content
                articles.append({'Title': title,
                                'Author': author,
                                'Date': date,
                                'Article': article,
                                'Link': link})
        else:
            logger.info(f"Scraping stopped")
            status = False
            break
    
    time.sleep(3)
    i+=1

# Save articles to CSV
save_articles_to_csv(articles)