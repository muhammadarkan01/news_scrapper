import pandas
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import logging

def setup_logger():
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

    return logger

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses
    return bs(response.text, 'html.parser')

def date_converter(date_raw):
    date_string_cleaned = date_raw.split(",")[1].strip().replace("WIB", "").strip()
    return datetime.strptime(date_string_cleaned, '%d %b %Y %H:%M')

def get_article(url, logger):
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

def save_articles_to_csv(articles, filename="articles.csv", logger=None):
    try:
        df = pandas.DataFrame(articles)
        df.to_csv(filename, index=False)
        if logger:
            logger.info(f"Articles successfully saved to {filename}")
    except Exception as e:
        if logger:
            logger.error(f"Error occurred while saving articles to CSV: {e}")

def scrape_index_page(url, date_now, logger):
    articles = []
    try:
        soup = get_soup(url)
        news_contents = soup.find_all('article', class_='list-content__item')

        for content in news_contents:
            link = content.find('a')['href']

            date_raw = content.find('div', class_='media__date').find('span')['title']
            date = date_converter(date_raw)

            date_delta = date_now - date
            date_delta_minutes = date_delta.total_seconds() / 60

            if date_delta_minutes < 60.0:
                logger.info(f"Scraping article: {link}")
                logger.info(f"Article date: {date}")
                title, author, date, article = get_article(link, logger)
                if title and article:  # Append only if there's valid content
                    articles.append({'Title': title,
                                    'Author': author,
                                    'Date': date,
                                    'Article': article,
                                    'Link': link})
            else:
                logger.info(f"Scraping stopped due to date exceeding threshold.")
                return articles, False
        
        return articles, True
    except Exception as e:
        logger.error(f"Error occurred while scraping index page {url}: {e}")
        return articles, False

def main():
    logger = setup_logger()
    articles = []
    date_now = datetime.now()
    i = 1
    status = True

    while status:
        url = f'https://oto.detik.com/indeks?page={i}'
        logger.info(f"Scraping page: {url}")

        new_articles, status = scrape_index_page(url, date_now, logger)
        articles.extend(new_articles)

        time.sleep(3)  # Pause to avoid overwhelming the server
        i += 1

    # Save articles to CSV
    save_articles_to_csv(articles, logger=logger)

if __name__ == "__main__":
    main()
