import abc
from statistics import mean
from scraper import abc_scraper
from models import vadar
import pandas as pd
from db import postgres
from os import environ

def average_key_point_sentiment(key_points: list):
    if key_points is None:
        return None
    return mean([vadar.compound_score(kp) for kp in key_points])

if __name__ == "__main__":

    for offset in range(0, 200, 25):
        # Get abc articles
        article_list = abc_scraper.get_list_articles(offset=offset)
        parsed_article_list = abc_scraper.parse_article_list(article_list)
        articles = pd.DataFrame(parsed_article_list)
        
        # Get article soups
        articles['soup'] = articles.link.apply(abc_scraper.get_article_soup)
        
        # Get metadata from articles
        articles['tags'] = articles.soup.apply(abc_scraper.get_tags)
        articles['content'] = articles.soup.apply(abc_scraper.get_content)
        articles['key_points'] = articles.soup.apply(abc_scraper.get_key_points)

        # Perform sentiment analysis
        articles['title_sentiment'] = articles.title.apply(vadar.compound_score)
        articles['key_points_sentiment'] = articles.key_points.apply(average_key_point_sentiment)

        # Connect to database
        conn = postgres.connect_to_database(environ.get('POSTGRES_USER'), 
                                            environ.get('POSTGRES_PASSWORD'),
                                            environ.get('POSTGRES_HOST'),
                                            environ.get('POSTGRES_DATABASE_NAME'))

        # Insert into database
        postgres.insert(articles.drop('soup', axis=1), conn)
    