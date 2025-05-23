# Import
import time 
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Made module
from setuppers.logger import setup_logger
# from setuppers.setup_schedule import setup_schedule
from converters.csv_converter import save_articles_to_csv, generate_summary
from scrappers.getting_articles import scrape_index_page

from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import time

def scrape_pages_concurrently(pages, date_target, logger):
    articles = []
    status = True

    # Define the scrape function to apply
    scrape_func = lambda page: scrape_index_page(f'https://oto.detik.com/indeks?page={page}', date_target, logger)

    # Use ThreadPoolExecutor to scrape pages concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust `max_workers` as needed
        results = executor.map(scrape_func, pages)

        for new_articles, task_status in results:
            articles.extend(new_articles)
            if not task_status:  # Stop scraping if the status is False
                status = False
                break

    return articles, status

def main(logger):
    articles = []
    date_target = datetime.datetime(2025, 2, 9)
    i = 1
    status = True

    while status:
        # Create a list of pages to scrape concurrently
        pages = list(range(i, i + 5))  # Scrape 5 pages concurrently, adjust as needed
        new_articles, status = scrape_pages_concurrently(pages, date_target, logger)
        articles.extend(new_articles)

        time.sleep(3)  # Optional delay
        i += 5  # Move to the next batch of pages

    # Save articles to CSV
    save_articles_to_csv(articles, logger=logger)
    
    summarize = input("Do you want to summarize each text ? (y/n)").lower()
    if summarize == 'y' or summarize =='yes':
        logger.info("Summarizing articles")
        df = pd.read_csv('articles.csv')
        df['Summary'] = df['Article'].apply(lambda x: generate_summary(x))
        df.to_csv('articles_summarized.csv', index=False)
    else:
        logger.info(f"News are scrapped and summarized up to {date_target}")

if __name__ == "__main__":
    logger = setup_logger()
    main(logger)

