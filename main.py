# Import
import time 
from datetime import datetime

# Made module
from setuppers.logger import setup_logger
from setuppers.setup_schedule import setup_schedule
from converters.csv_converter import save_articles_to_csv
from scrappers.getting_articles import scrape_index_page


def main(logger):
    logger = logger
    articles = []
    date_now = datetime.now()
    i = 1
    status = True

    while status:
        url = f'https://oto.detik.com/indeks?page={i}'
        logger.info(f"Scraping page: {url}")

        new_articles, status = scrape_index_page(url, date_now, logger)
        articles.extend(new_articles)

        time.sleep(3)  
        i += 1

    # Save articles to CSV
    save_articles_to_csv(articles, logger=logger)

if __name__ == "__main__":
    logger = setup_logger()
    setup_schedule(main, logger)

