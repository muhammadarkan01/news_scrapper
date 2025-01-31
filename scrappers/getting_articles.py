from converters.date_converter import date_converter
from scrappers.get_soup import get_soup
import time

def get_article(url:str, logger): 
    # Add type hints, to be explained later at the code quality module
    try:
        soup = get_soup(url)
        content = soup.find('div', class_='column-8')

        # Extract title
        if content and content.find('h1', class_='detail__title'):
            title = content.find('h1', class_='detail__title').text.strip()
        else:
            None

        # Extract author
        if content and content.find('div', class_='detail__author'):
            author = content.find('div', class_='detail__author').text.strip()
        else:
            None

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


def scrape_index_page(url:str, date_target, logger):
    articles = []
    
    try:
        soup = get_soup(url)
        news_contents = soup.find_all('article', class_='list-content__item')

        for content in news_contents:
            link = content.find('a')['href']

            date_raw = content.find('div', class_='media__date').find('span')['title']
            date = date_converter(date_raw)

            if date >= date_target:
                logger.info(f"Scraping article: {link}")
                logger.info(f"Article date: {date}")
                title, author, date, article = get_article(link, logger)
                if title and article:  # Append only if there's valid content
                    articles.append({'Title': title,
                                    'Author': author,
                                    'Date': date,
                                    'Article': article,
                                    'Link': link})
                    time.sleep(2)
            else:
                logger.info(f"Scraping stopped due to date exceeding threshold.")
                return articles, False
            
        return articles, True

    except Exception as e:
        logger.error(f"Error occurred while scraping index page {url}: {e}")
        return articles, False