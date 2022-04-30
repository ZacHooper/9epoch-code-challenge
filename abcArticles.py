import abc
from statistics import mean
from scraper import abc_scraper
from models import vadar
import pandas as pd

def average_key_point_sentiment(key_points: list):
    if key_points is None:
        return None
    return mean([vadar.compound_score(kp) for kp in key_points])

if __name__ == "__main__":
    article_list = abc_scraper.get_list_articles()
    parsed_article_list = abc_scraper.parse_article_list(article_list)
    articles = pd.DataFrame(parsed_article_list[0:3])
    articles['soup'] = articles.link.apply(abc_scraper.get_article_soup)

    articles['tags'] = articles.soup.apply(abc_scraper.get_tags)
    articles['content'] = articles.soup.apply(abc_scraper.get_content)
    articles['key_point'] = articles.soup.apply(abc_scraper.get_key_points)

    articles['title_sentiment'] = articles.title.apply(vadar.compound_score)
    articles['key_point_sentiment'] = articles.key_point.apply(average_key_point_sentiment)
    
    