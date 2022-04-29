import requests
import bs4
import json

def get_list_articles(offset: int = 0, size: int = 25, total: int = 250):
    """Get's a JSON document containing a collection of the articles on the "just in" page of the ABC website. 

    Args:
        offset (int, optional): Moves the "size" cursor by 1 through the total list of articles. Defaults to 0.
        size (int, optional): How many articles are returned in the JSON payload. Defaults to 25.
        total (int, optional): How many articles are queried for. Defaults to 250.

    Returns:
        JSON : The raw JSON response of the article
    """
    payload = {
        "offset": offset,
        "size": size,
        "total": total
    }
    r = requests.get("https://www.abc.net.au/news-web/api/loader/justinstories", params=payload)
    return r.json()

def get_article_soup(link: str):
    """Get's an article and turns it into Beautifulsoup ready for further investigation.

    Args:
        link (str): link to the news article

    Returns:
        BeautifulSoup: A BeautifulSoup object
    """
    r = requests.get(f"https://www.abc.net.au{link}")
    if not r.ok:
        r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup

get_title = lambda article: article['title']['children'].strip()
get_link = lambda article: article['link']['to']

def get_authors(article):
    """Get's list of authors for article. If none found returns None object"""
    authors = article['newsBylineProps']['authors']
    if authors is None:
        return None
    return [author['name'] for author in authors]

get_description = lambda article: article['synopsis']
get_published = lambda article: article['timestamp']['dates']['firstPublished']['labelDate']

def get_last_updated(article):
    """Get's the last updated timestamp from JSON object"""
    if article['timestamp']['dates']['lastUpdated'] is None:
        return None
    else:
        return article['timestamp']['dates']['lastUpdated']['labelDate'] 

def clean_article(article):
    return {
        "title": get_title(article),
        "link": get_link(article),
        "author": get_authors(article),
        "description": get_description(article),
        "published": get_published(article),
        "last_updated": get_last_updated(article)
    }

def parse_article_list(article_list: dict):
    """Parses the initial article JSON list.

    Args:
        article_list (dict): JSON object of articles

    Returns:
        list: List of articles as dict objects
    """
    
    dirty_articles = article_list['collection']
    articles = [clean_article(article) for article in dirty_articles]
    return articles


if __name__ == "__main__":
    articles = get_list_articles(1)
    print(len(articles['collection']))
    with open('example_article_list.json', 'w') as outfile:
        outfile.write(json.dumps(articles))

    clean_articles = parse_article_list(articles)
    print(clean_articles)