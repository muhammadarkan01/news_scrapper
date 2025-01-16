import pandas as pd
from pathlib import Path

def save_articles_to_csv(articles, filename="articles.csv", logger=None):
    the_file = Path(filename)
    if the_file.exists():    
        try:
            df1 = pd.read_csv(filename)
            df2 = pd.DataFrame(articles)
            df = pd.concat([df1, df2])
            df = df.drop_duplicates(subset=['Title'])

            df.to_csv(filename, index=False)

            if logger:
                logger.info(f"Articles successfully added to {filename}")
        except Exception as e:
            if logger:
                logger.error(f"Error occurred while adding articles to CSV: {e}")
    else:    
        try:
            df = pd.DataFrame(articles)

            df.to_csv(filename, index=False)

            if logger:
                logger.info(f"Articles successfully created to {filename}")
        except Exception as e:
            if logger:
                logger.error(f"Error occurred while creating articles to CSV: {e}")